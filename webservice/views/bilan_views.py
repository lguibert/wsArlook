# -*- coding: utf-8 -*-
from general_views import send_response
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from calendar import monthrange

# ----------------------------------------             ----------------------------------------
# ---------------------------------------- BILAN ----------------------------------------
# ----------------------------------------             ----------------------------------------

@csrf_exempt
def get_bilan(request):
    if request.method == "POST":
        date = datetime.datetime.strptime(request.body, '%Y-%m-%d')

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
                    final[str(user[0])][1].append({i: "Rien"})
            else:
                try:
                    final[str(user[0])][1][0]['' + i + ''] = user[2]
                except IndexError:
                    final[str(user[0])][1][0]['' + i + ''] = "Rien"

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
            "SELECT u.id, u.username, sum(s.price + s.price * t.tva_value / 100) as 'Sell' "
            "from arlook.webservice_sell as s  inner join webservice_tva as t on s.tva_id = t.id  "
            "inner join auth_user as u on s.user_id = u.id where s.date between %s and %s group by user_id",
            [min, max])
    else:
        cursor.execute(
            "SELECT u.id, u.username, sum(s.price + s.price * t.tva_value / 100) as 'Sell' "
            "from arlook.webservice_sell as s  inner join webservice_tva as t on s.tva_id = t.id  "
            "inner join auth_user as u on s.user_id = u.id group by user_id")

    results = cursor.fetchall()

    if len(results) == 0:
        cursor.execute(
            "SELECT u.id, u.username from arlook.webservice_sell as s inner join auth_user as u on s.user_id = u.id group by user_id")

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
        date = datetime.datetime.strptime(request.body, '%Y-%m-%d')

        visit_day = get_visited_bilan("day", date)
        visit_week = get_visited_bilan("week", date)
        visit_month = get_visited_bilan("month", date)
        visit_all = get_visited_bilan("all")
        all = [visit_day, visit_week, visit_month, visit_all]

        final = data_bilan_layout(all)

        return send_response(final)
    else:
        visit_day = get_visited_bilan("day")
        visit_week = get_visited_bilan("week")
        visit_month = get_visited_bilan("month")
        visit_all = get_visited_bilan("all")
        all = [visit_day, visit_week, visit_month, visit_all]

        final = data_bilan_layout(all)

    return send_response(final)


def get_visited_bilan(type, date=None):
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
            "SELECT u.id, u.username, count(v.id) from arlook.webservice_visit as v inner join auth_user as u on v.user_id = u.id where v.visit_date between %s and %s group by user_id",
            [min, max])
    else:
        cursor.execute(
            "SELECT u.id, u.username, count(v.id) from arlook.webservice_visit as v inner join auth_user as u on v.user_id = u.id  group by user_id")

    results = cursor.fetchall()

    if len(results) == 0:
        cursor.execute(
            "SELECT u.id, u.username from arlook.webservice_visit as v inner join auth_user as u on v.user_id = u.id group by user_id")

        results = cursor.fetchall()

    return results
