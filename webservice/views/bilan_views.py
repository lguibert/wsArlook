# -*- coding: utf-8 -*-
from general_views import send_response
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from calendar import monthrange
import json
from webservice.models import User
from django.utils.html import escape


# ----------------------------------------             ----------------------------------------
# ---------------------------------------- BILAN ----------------------------------------
# ----------------------------------------             ----------------------------------------

@csrf_exempt
def get_bilan(request):
    if request.method == "POST":
        date = datetime.datetime.strptime(escape(request.body), '%Y-%m-%d')

        prod_lines_day = get_typed_bilan("day", date)
        prod_lines_week = get_typed_bilan("week", date)
        prod_lines_month = get_typed_bilan("month", date)
        prod_lines_all = get_typed_bilan("all")
        all = [prod_lines_day, prod_lines_week, prod_lines_month, prod_lines_all]

        final = data_bilan_layout(all)

        return send_response(final)
    else:
        prod_lines_day = get_typed_bilan("day")
        prod_lines_week = get_typed_bilan("week")
        prod_lines_month = get_typed_bilan("month")
        prod_lines_all = get_typed_bilan("all")
        all = [prod_lines_day, prod_lines_week, prod_lines_month, prod_lines_all]

        final = data_bilan_layout(all)

    return send_response(final)


def data_bilan_layout(all):
    final = {}

    for i, arrays in enumerate(all):
        i = index_to_type(i)
        for user in arrays:
            if not str(user[0]) in final:
                final[str(user[0])] = [user[1], []]
                try:
                    final[str(user[0])][1].append({i: user[2]})
                except IndexError:
                    final[str(user[0])][1].append({i: 0})
            else:
                try:
                    final[str(user[0])][1][0]['' + i + ''] = user[2]
                except IndexError:
                    final[str(user[0])][1][0]['' + i + ''] = 0

    return final


def index_to_type(index):
    if index == 0:
        return "day"
    elif index == 1:
        return "week"
    elif index == 2:
        return "month"
    elif index == 3:
        return "all"
    else:
        return None


def execute_bilan_query(min=None, max=None, all=False):
    cursor = connection.cursor()
    if not all:
        cursor.execute(
            "SELECT u.id, u.username, sum(s.price * s.qte) as 'Sell' "
            "from arlook.webservice_sell as s "
            "inner join auth_user as u on s.user_id = u.id where s.date between %s and %s group by user_id",
            [min, max])
    else:
        cursor.execute(
            "SELECT u.id, u.username, sum(s.price * s.qte) AS 'Sell' "
            "FROM arlook.webservice_sell AS s INNER JOIN auth_user AS u ON s.user_id = u.id GROUP BY user_id")

    results = cursor.fetchall()

    if len(results) == 0:
        cursor.execute(
            "SELECT u.id, u.username FROM arlook.webservice_sell AS s "
            "INNER JOIN auth_user AS u ON s.user_id = u.id GROUP BY user_id")

        results = cursor.fetchall()

    return results


def get_typed_bilan(type, date=None):
    if not date:
        date = datetime.date.today()

    if type == "day" or type == "undefined":
        today_min = datetime.datetime.combine(date, datetime.time.min)
        today_max = datetime.datetime.combine(date, datetime.time.max)
        prod_lines = execute_bilan_query(today_min, today_max)

    elif type == "week":
        start = date - datetime.timedelta(days=date.weekday())
        end = date + datetime.timedelta(days=6 - date.weekday())
        prod_lines = execute_bilan_query(start, end)

    elif type == "month":
        start = date - datetime.timedelta(days=date.day - 1)
        end = date + datetime.timedelta(days=monthrange(date.year, date.month)[1] - date.day)
        prod_lines = execute_bilan_query(start, end)

    elif type == "all":
        prod_lines = execute_bilan_query(all=True)

    else:
        prod_lines = None

    return prod_lines


# ----------------------------------------             ----------------------------------------
# ---------------------------------------- VISIT BILAN ----------------------------------------
# ----------------------------------------             ----------------------------------------

@csrf_exempt
def get_bilan_visit(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id_user = User.objects.get(username=data[0]).id
        date = data[1]
        if date:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')

            visit_day = get_visited_bilan("day", id_user, date=date)
            visit_week = get_visited_bilan("week", id_user, date=date)
            visit_month = get_visited_bilan("month", id_user, date=date)
            visit_all = get_visited_bilan("all", id_user)
            all = [visit_day, visit_week, visit_month, visit_all]
            typespay = get_typepay_bilan_all(date=date)

            final = data_bilan_layout_visit(all)
            final_pay = data_typepay_layout_visit(typespay)

        else:
            visit_day = get_visited_bilan("day", id_user)
            visit_week = get_visited_bilan("week", id_user)
            visit_month = get_visited_bilan("month", id_user)
            visit_all = get_visited_bilan("all", id_user)
            all = [visit_day, visit_week, visit_month, visit_all]
            typespay = get_typepay_bilan_all()

            final = data_bilan_layout_visit(all)
            final_pay = data_typepay_layout_visit(typespay)

    return send_response([final, final_pay])


def get_visited_bilan(type, id_user=None, date=None):
    if not date:
        date = datetime.date.today()

    if type == "day" or type == "undefined":
        today_min = datetime.datetime.combine(date, datetime.time.min)
        today_max = datetime.datetime.combine(date, datetime.time.max)
        visit_lines = execute_visit_query(today_min, today_max)

    elif type == "week":
        start = date - datetime.timedelta(days=date.weekday())
        end = date + datetime.timedelta(days=6 - date.weekday())
        visit_lines = execute_visit_query(start, end)

    elif type == "month":
        start = date - datetime.timedelta(days=date.day - 1)
        end = date + datetime.timedelta(days=monthrange(date.year, date.month)[1] - date.day)
        visit_lines = execute_visit_query(start, end)

    elif type == "all":
        visit_lines = execute_visit_query(all=True)

    else:
        visit_lines = None

    return visit_lines


def execute_visit_query(min=None, max=None, all=False):
    cursor = connection.cursor()
    if not all:
        cursor.execute(
            "SELECT u.id, u.username, sum(v.value), count(v.id) from arlook.webservice_visit as v inner join auth_user as u on v.user_id = u.id where v.visit_date between %s and %s group by user_id",
            [min, max])
    else:
        cursor.execute(
            "SELECT u.id, u.username, sum(v.value), count(v.id) FROM arlook.webservice_visit AS v INNER JOIN auth_user AS u ON v.user_id = u.id  GROUP BY user_id")

    results = cursor.fetchall()

    if len(results) == 0:
        cursor.execute(
            "SELECT u.id, u.username FROM arlook.webservice_visit AS v INNER JOIN auth_user AS u ON v.user_id = u.id GROUP BY user_id")

        results = cursor.fetchall()

    return results


def data_bilan_layout_visit(all):
    final = {}

    for i, arrays in enumerate(all):
        i = index_to_type(i)
        for user in arrays:
            str_user = str(user[0])
            if not str_user in final:
                final[str_user] = [user[1], user[0], []]
                try:
                    final[str_user][2].append({i: [user[2], user[3]]})
                except IndexError:
                    final[str_user][2].append({i: [0, 0]})
            else:
                try:
                    final[str_user][2][0]['' + i + ''] = [user[2], user[3]]
                except IndexError:
                    final[str_user][2][0]['' + i + ''] = [0, 0]

    return final


# ---------------------------------------------- TYPE PAY --------------------------------------------------------------
def get_user_ids():
    return User.objects.all().values("id")


def get_typepay_bilan_all(id_user=None, date=None):
    if not date:
        date = datetime.date.today()

    pays = {}

    if id_user is None:
        users = get_user_ids()

        for id in users:
            id_user = str(id['id'])

            today_min = datetime.datetime.combine(date, datetime.time.min)
            today_max = datetime.datetime.combine(date, datetime.time.max)
            typepay_day = execute_typepay_query(id_user, today_min, today_max)

            start = date - datetime.timedelta(days=date.weekday())
            end = date + datetime.timedelta(days=6 - date.weekday())
            typepay_week = execute_typepay_query(id_user, start, end)

            start = date - datetime.timedelta(days=date.day - 1)
            end = date + datetime.timedelta(days=monthrange(date.year, date.month)[1] - date.day)
            typepay_month = execute_typepay_query(id_user, start, end)

            typepay_all = execute_typepay_query(id_user, all=True)

            pays[id_user] = [typepay_day, typepay_week, typepay_month, typepay_all]
    else:
        today_min = datetime.datetime.combine(date, datetime.time.min)
        today_max = datetime.datetime.combine(date, datetime.time.max)
        typepay_day = execute_typepay_query(id_user, today_min, today_max)

        start = date - datetime.timedelta(days=date.weekday())
        end = date + datetime.timedelta(days=6 - date.weekday())
        typepay_week = execute_typepay_query(id_user, start, end)

        start = date - datetime.timedelta(days=date.day - 1)
        end = date + datetime.timedelta(days=monthrange(date.year, date.month)[1] - date.day)
        typepay_month = execute_typepay_query(id_user, start, end)

        typepay_all = execute_typepay_query(id_user, all=True)

        pays[id_user] = [typepay_day, typepay_week, typepay_month, typepay_all]

    return pays


def execute_typepay_query(id_user, min=None, max=None, all=False):
    cursor = connection.cursor()
    if not all:
        cursor.execute(
            "SELECT u.id, u.username, ifnull(v.typepay_id,0), ifnull(count(typepay_id),0) from webservice_visit AS v INNER JOIN auth_user AS u ON v.user_id = u.id where user_id = %s and visit_date between %s and %s group by typepay_id",
            [id_user, min, max])
    else:
        cursor.execute(
            "SELECT u.id, u.username, ifnull(v.typepay_id,0), ifnull(count(typepay_id),0) from webservice_visit AS v INNER JOIN auth_user AS u ON v.user_id = u.id where user_id = %s group by typepay_id",
            [id_user])

    results = cursor.fetchall()

    if len(results) == 0:
        cursor.execute(
            "SELECT u.id, u.username FROM arlook.auth_user AS u where u.id = %s GROUP BY u.id", [id_user])

        results = cursor.fetchall()

    return [results]


def data_typepay_layout_visit(typespay):
    final = {}
    users = get_user_ids()
    for id in users:
        user_id = str(id['id'])
        for i, data in enumerate(typespay[user_id]):
            i = index_to_type(i)
            for t in data:
                if not user_id in final:
                    final[user_id] = {i: {}}
                    for d in t:
                        try:
                            final[user_id][i][typeid_to_name(d[2])] = d[3]
                        except:
                            pass
                        if not typeid_to_name(1) in final[user_id][i]:
                            final[user_id][i][typeid_to_name(1)] = 0
                        if not typeid_to_name(2) in final[user_id][i]:
                            final[user_id][i][typeid_to_name(2)] = 0
                        if not typeid_to_name(3) in final[user_id][i]:
                            final[user_id][i][typeid_to_name(3)] = 0
                else:
                        final[user_id][i] = {}
                        for d in t:
                            try:
                                if not i in final[user_id]:
                                    final[user_id][i] = {typeid_to_name(d[2]): d[3]}
                                else:
                                    final[user_id][i][typeid_to_name(d[2])] = d[3]
                            except:
                                pass
                            if not typeid_to_name(1) in final[user_id][i]:
                                final[user_id][i][typeid_to_name(1)] = 0
                            if not typeid_to_name(2) in final[user_id][i]:
                                final[user_id][i][typeid_to_name(2)] = 0
                            if not typeid_to_name(3) in final[user_id][i]:
                                final[user_id][i][typeid_to_name(3)] = 0

    return final


def typeid_to_name(type_id):
    type_id = str(type_id)
    if type_id == '1':
        return "cb"
    elif type_id == '2':
        return "cheque"
    elif type_id == '3':
        return "espece"
    else:
        return None
