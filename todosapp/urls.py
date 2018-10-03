#from django.conf.urls import include
from django.urls import path, re_path, include
from hello import hello
# from menus.simpleMenu import respondwithmenu
from menus import views


urlpatterns = [
    re_path(r'^todos/', include('todos.urls')),
    path('hello/<int:mynumber>/', hello.sendhellonumber),

    # path('menus/<str:restaurant_name>', include('menus.urls'))
    path('menus/<str:restaurant_name>', views.menu_detail)

]
