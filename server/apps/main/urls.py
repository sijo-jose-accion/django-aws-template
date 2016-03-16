from django.conf.urls import *
from django.views.decorators.cache import cache_page

from .views import *


urlpatterns = patterns('',
     url(r'^$', HomeIndexView.as_view(), name='home'),
     url(r'^message/send/$', ContactCreateView.as_view(), name='send-message'),
     # ---------------------------------
     url(r'^jsi18n', 'apps.main.views.i18n_javascript'),
     url(r'^admin/jsi18n', 'apps.main.views.i18n_javascript'),
     url(r'^i18n/', include('django.conf.urls.i18n')),
     url(r'^robots.txt$', RobotView.as_view()),
     url(r'^crossdomain.xml$', CrossDomainView.as_view()),
)
