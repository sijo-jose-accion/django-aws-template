from django.conf.urls import *

from .views import *

urlpatterns = [

     url(r'^', include('allauth.urls')),
     url(r'^$', AccountRedirectView.as_view(), name='account_redirect'),
     url(r'^(?P<slug>[^/]+)/edit/$', AccountUpdateView.as_view(), name='account_edit'),
     url(r'^(?P<slug>[^/]+)/$', AccountDetailView.as_view(), name='account_detail'),
]
