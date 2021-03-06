# -*- coding: utf-8 -*-
from general_views import send_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
import json
from webservice.models import User
from django.contrib.auth.hashers import make_password
from webservice.views.bilan_views import get_visited_bilan, index_to_type, get_typed_bilan, get_typepay_bilan_all, typeid_to_name
import datetime


@csrf_exempt
def update_password(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            user = User.objects.get(username=data[1])

            user.password = make_password(data[0])

            user.save()

            return send_response(True)
        except:
            return send_response("Erreur lors du changement de mot de passe.", 500)


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return send_response([user.username, user.password, "admin"])
            else:
                return send_response([user.username, user.password, "user"])
        else:
            return send_response("Erreur d'identifiant", 500)
    else:
        return send_response("", 500)


@csrf_exempt
def new_user(request):
    if request.method == "POST":
        newuser = json.loads(request.body)

        try:
            user = User()
            user.password = make_password(newuser['password'])
            user.username = newuser['name']
            user.first_name = newuser['name']
            user.is_superuser = newuser['superuser']
            user.save()

            return send_response(True)
        except:
            return send_response("Erreur lors de la création de l\'utilisateur", 500)


@csrf_exempt
def user_presta(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = User.objects.get(username=data[0])
        if data[1]:
            date = datetime.datetime.strptime(data[1], '%Y-%m-%d')
        else:
            date = None

        #try:
        if date is None:
            visit_day = get_visited_bilan("day")
            visit_week = get_visited_bilan("week")
            visit_month = get_visited_bilan("month")
            visit_all = get_visited_bilan("all")
            pays = get_typepay_bilan_all(user.id)

            all = [visit_day, visit_week, visit_month, visit_all]

        else:
            visit_day = get_visited_bilan("day", date=date)
            visit_week = get_visited_bilan("week", date=date)
            visit_month = get_visited_bilan("month", date=date)
            visit_all = get_visited_bilan("all")
            pays = get_typepay_bilan_all(user.id, date=date)
            all = [visit_day, visit_week, visit_month, visit_all]

        final_pay = data_typepay_layout_visit(pays, user.id)
        final = data_bilan_layout(all, user.id)

        return send_response([final, final_pay])
        #except:
        #    return send_response("Erreur lors de la récupération des données.", 500)


@csrf_exempt
def user_sell(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = User.objects.get(username=data[0])
        if data[1]:
            print data[1]
            date = datetime.datetime.strptime(data[1], '%Y-%m-%d')
        else:
            date = None

        try:
            if date is None:
                visit_day = get_typed_bilan("day")
                visit_week = get_typed_bilan("week")
                visit_month = get_typed_bilan("month")
                visit_all = get_typed_bilan("all")

                all = [visit_day, visit_week, visit_month, visit_all]

            else:
                visit_day = get_typed_bilan("day", date)
                visit_week = get_typed_bilan("week", date)
                visit_month = get_typed_bilan("month", date)
                visit_all = get_typed_bilan("all")
                all = [visit_day, visit_week, visit_month, visit_all]

            final = data_bilan_layout(all, user.id)

            return send_response(final)
        except:
            return send_response("Erreur lors de la récupération des données.", 500)


def data_bilan_layout(all, user_id):
    final = {}

    for i, arrays in enumerate(all):
        i = index_to_type(i)
        for user in arrays:
            f_user = str(user[0])
            if not f_user in final and f_user == str(user_id):
                final[f_user] = [user[1], user[0], []]
                try:
                    final[f_user][2].append({i: user[2]})
                except IndexError:
                    final[f_user][2].append({i: "Rien"})
            elif f_user in final and f_user == str(user_id):
                try:
                    final[f_user][2][0]['' + i + ''] = user[2]
                except (IndexError, KeyError):
                    final[f_user][2][0]['' + i + ''] = "Rien"
    return final


def data_typepay_layout_visit(typespay, user_id):
    final = {}
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


@csrf_exempt
def user_loginbilan(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data[0]
        password = data[1]

        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return send_response(True)
        else:
            return send_response("Erreur d'identifiant", 500)
