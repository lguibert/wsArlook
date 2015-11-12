from django.conf.urls import url, patterns

urlpatterns = patterns('webservice.views',
                       url(r'products/add/?', 'new_product'),

                       url(r'products/?', 'get_products'),


                       url(r'product/in/store/?', 'in_product_store'),
                       url(r'product/out/store/?', "out_product_store"),
                       url(r'product/in/?', 'in_product'),
                       url(r'product/out/?', "out_product"),
                       url(r'product/update/?', 'update_product'),
                       url(r'product/line/(?P<uuid>[a-zA-Z0-9]{1,})/?', 'line_prod'),
                       url(r'product/(?P<uuid>[a-zA-Z0-9]{1,})/?', 'get_product'),


                       url(r'tva/?', 'get_tva'),

                       url(r'clients/add/?', 'new_client'),
                       url(r'clients/?', 'get_clients'),
                       url(r'client/update/?', 'update_client'),
                       url(r'client/line/(?P<uuid>[a-zA-Z0-9]{1,})/?', 'line_client'),
                       url(r'client/(?P<uuid>[a-zA-Z0-9]{1,})/?', 'get_client'),

                       url(r'login/?', 'login'),

                       )
