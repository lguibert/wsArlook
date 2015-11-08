# -*- coding: utf-8 -*-
from general_views import send_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
import json


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
