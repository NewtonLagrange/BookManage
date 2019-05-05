from django.conf.urls import url
from . import views
from django.views.generic.base import RedirectView

# comment urls
app_name = 'login'
urlpatterns = [
    url(r'^$', views.comment, name='comment'),
    url(r'^favicon\.ico$', RedirectView.as_view(url=r'static/img/favicon.ico')),
]