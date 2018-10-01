#from django.conf.urls import url, include
from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from todos import views


urlpatterns = {
    re_path(r'^$', views.TodoList.as_view(), name='list'),
    re_path(r'^(?P<pk>[0-9]+)/$', views.TodoDetail.as_view(), name='details'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
