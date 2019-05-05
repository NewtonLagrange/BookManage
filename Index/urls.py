from django.conf.urls import url
from . import views
from django.views.generic.base import RedirectView

# login urls
app_name = 'login'
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'^verify/.*?$', views.verify, name='verify'),
    url(r'^verify_code/$', views.verify_code, name='verify_code'),
    url(r'^favicon\.ico$', RedirectView.as_view(url=r'static/img/favicon.ico')),
]
