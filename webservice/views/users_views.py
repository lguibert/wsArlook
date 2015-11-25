# -*- coding: utf-8 -*-
from general_views import send_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
import json
from webservice.models import User
from django.contrib.auth.hashers import make_password


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
            if 'email' in newuser:
                user.email = newuser['email']
            user.is_superuser = newuser['superuser']
            user.save()

            return send_response(True)
        except:
            return send_response("Erreur lors de la création de l\'utilisateur", 500)
