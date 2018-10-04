from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics
from menus.serializers import MenuSerializer
from menus.models import Menu
import datetime
from menus.simpleMenu import cache_menu, restaurants_dict2
import traceback


@csrf_exempt
def menu_detail(request, restaurant_name):

    date_now = datetime.date.today()
    try:
        restaurant = restaurants_dict2[restaurant_name]
        # print(restaurant)
        menus = get_menus_for(restaurant, date_now)

        serializer = MenuSerializer(menus, many=True)
        return JsonResponse(serializer.data, safe=False)

    except KeyError:
        traceback.print_exc()
        return HttpResponse(status=404)

    # old stuff for fetching only a single menu item from db
    # try:
        # dbmenu = Menu.objects.get(restaurant_id=490051, menu_date=date_now)
    #    menus = Menu.objects.filter(restaurant_id=490051, menu_date=date_now)
    # except Menu.DoesNotExist:
    #    cache_menu(restaurant_name, date_now)
    #    menus = Menu.objects.filter(restaurant_id=490051, menu_date=date_now)


def get_menus_for(restaurant, date):

    menus = Menu.objects.filter(restaurant_id=restaurant["restaurant_id"], menu_date=date)
    # we don't have menus for the date yet for this restaurant, cache them them
    if len(menus) < 1:
        cache_menu(restaurant, date)
        menus = Menu.objects.filter(restaurant_id=restaurant["restaurant_id"], menu_date=date)

    return menus

# class Menu(generics.ListCreateAPIView):
#    queryset = Menus.objects.all()
#    serializer_class = TodoSerializer

#    def perform_create(self, serializer):
#        print("saving a new menu item")
#        serializer.save()
