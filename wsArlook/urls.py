"""wsArlook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, patterns

urlpatterns = patterns('webservice.views',
                       url(r'products/add?', 'new_product'),
                       url(r'products/?', 'get_products'),
                       url(r'product/(?P<uuid>[a-zA-Z0-9]{1,})/?', 'get_product'),

                       url(r'tva/?', 'get_tva'),

                       url(r'clients/add?', 'new_client'),
                       url(r'clients/?', 'get_clients'),
                       url(r'client/(?P<uuid>[a-zA-Z0-9]{1,})/?', 'get_client'),

                       url(r'login/?', 'login'),

                       )