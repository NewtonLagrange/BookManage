from django.conf.urls import url
from . import views
from django.views.generic.base import RedirectView

app_name = 'Book'
urlpatterns = [
    url(r'^book/$', views.book, name='book'),
    url(r'^borrow/(\d+)/$', views.borrow, name='borrow'),
    url(r'^user_info/$', views.user_info, name='user_info'),
    url(r'^borrow_record/$', views.borrow_record, name='borrow_record'),
    url(r'^search/$', views.search, name='search'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^ajax/$', views.ajax, name='ajax'),
    url(r'^test/$', views.test, name='test'),
    url(r'^favicon\.ico$', RedirectView.as_view(url=r'static/img/favicon.ico')),
]
