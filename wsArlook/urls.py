from django.conf.urls import url, patterns

urlpatterns = patterns('webservice.views',
                       url(r'products/add/?', 'new_product'),

                       url(r'products/?', 'get_products'),

                       url(r'product/in/?', 'in_product'),
                       url(r'product/out/?', "out_product"),
                       url(r'product/update/?', 'update_product'),
                       url(r'product/line/(?P<uuid>[a-zA-Z0-9]{1,})/?', 'line_prod'),
                       url(r'product/(?P<uuid>[a-zA-Z0-9]{1,})/?', 'get_product'),


                       url(r'tva/?', 'get_tva'),

                       url(r'clients/add/?', 'new_client'),
                       url(r'clients/?', 'get_clients'),
                       url(r'client/(?P<uuid>[a-zA-Z0-9]{1,})/?', 'get_client'),

                       url(r'login/?', 'login'),

                       )
