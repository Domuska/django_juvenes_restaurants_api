from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from menus.simpleMenu import respondwithmenu
from menus import views

urlpatterns = {
    path('', views.menu_detail)
}
