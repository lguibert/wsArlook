from webservice.models import Sell
from general_views import send_response, serialize
import datetime


def get_bilan(request, type):
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    prod_lines = Sell.objects.filter(date__range=(today_min, today_max))

    lines = []
    total = 0

    for line in prod_lines:
        total = total + line.price + (line.price * line.tva.tva_value / 100)

    lines.append(str(total))
    lines.append("25")
    lines.append("159")
    lines.append("999")
    lines.append("10")

    return send_response(lines)
