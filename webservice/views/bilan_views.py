from webservice.models import Sell
from general_views import send_response, serialize
import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from calendar import monthrange


@csrf_exempt
def get_bilan(request):
    if request.method == "POST":
        date = datetime.datetime.strptime(request.body, '%Y-%m-%dT%H:%M:%S.%fZ')
        prod_lines = get_typed_bilan("perfect", date)
        lines = [prod_lines]

        return send_response(lines)
    else:
        prod_lines_day = get_typed_bilan("day")
        prod_lines_week = get_typed_bilan("week")
        prod_lines_month = get_typed_bilan("month")
        prod_lines_all = get_typed_bilan("all")
        all = [prod_lines_day, prod_lines_week, prod_lines_month, prod_lines_all]

        final = {}

        for arrays in all:
            for user in arrays:
                if not str(user[0]) in final:
                    final[str(user[0])] = [user[1]]
                    final[str(user[0])].append(user[2])
                else:
                    final[str(user[0])].append(user[2])

    return send_response(final)


def execute_query(min=None, max=None, all=False):
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
            "inner join auth_user as u on s.user_id = u.id where s.date group by user_id")

    return cursor.fetchall()


def get_typed_bilan(type, date=None):
    if type == "day" or type == "undefined":
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        prod_lines = execute_query(today_min, today_max)

    elif type == "week":
        today = datetime.date.today()
        start = today - datetime.timedelta(days=today.weekday())
        end = today + datetime.timedelta(days=6 - today.weekday())
        prod_lines = execute_query(start, end)

    elif type == "month":
        today = datetime.date.today()
        start = today - datetime.timedelta(days=today.day - 1)
        end = today + datetime.timedelta(days=monthrange(today.year, today.month)[1] - today.day)
        prod_lines = execute_query(start, end)

    elif type == "all":
        today = datetime.date.today()
        prod_lines = execute_query(all=True)

    elif type == "perfect":
        today_min = datetime.datetime.combine(date, datetime.time.min)
        today_max = datetime.datetime.combine(date, datetime.time.max)
        prod_lines = execute_query(today_min, today_max)
    else:
        prod_lines = None

    return prod_lines


'''
#start = today - datetime.timedelta(days=today.day-1)
#end = today + datetime.timedelta(days=monthrange(today.year, today.month)[1]-today.day)
'''
