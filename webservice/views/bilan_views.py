from webservice.models import Sell
from general_views import send_response
import datetime
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_bilan(request):
    if request.method == "POST":
        date = datetime.datetime.strptime(request.body, '%Y-%m-%dT%H:%M:%S.%fZ')
        prod_lines = get_typed_bilan("perfect", date)
        lines = [get_total(prod_lines)]

        return send_response(lines)
    else:
        print "GET !"
        prod_lines_day = get_typed_bilan("day")
        prod_lines_week = get_typed_bilan("week")
        prod_lines_month = get_typed_bilan("month")
        prod_lines_year = get_typed_bilan("year")

        lines = [get_total(prod_lines_day), get_total(prod_lines_week), get_total(prod_lines_month),
                 get_total(prod_lines_year)]

        return send_response(lines)


def get_total(lines):
    total = 0
    for line in lines:
        total = total + line.price + (line.price * line.tva.tva_value / 100)

    return str(total)


def get_typed_bilan(type, date=None):
    if type == "day" or type == "undefined":
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        prod_lines = Sell.objects.filter(date__range=(today_min, today_max))
    elif type == "week":
        today = datetime.date.today()
        start = today - datetime.timedelta(days=today.weekday())
        end = today + datetime.timedelta(days=6-today.weekday())
        prod_lines = Sell.objects.filter(date__range=(start, end))
    elif type == "month":
        today = datetime.date.today()
        prod_lines = Sell.objects.filter(date__month=today.month)
    elif type == "year":
        today = datetime.date.today()
        prod_lines = Sell.objects.filter(date__year=today.year)
    elif type == "perfect":
        today_min = datetime.datetime.combine(date, datetime.time.min)
        today_max = datetime.datetime.combine(date, datetime.time.max)
        prod_lines = Sell.objects.filter(date__range=(today_min, today_max))
    else:
        prod_lines = None

    return prod_lines


'''
#start = today - datetime.timedelta(days=today.day-1)
#end = today + datetime.timedelta(days=monthrange(today.year, today.month)[1]-today.day)
'''