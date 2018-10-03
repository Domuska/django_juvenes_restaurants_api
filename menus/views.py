from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics
from menus.serializers import MenuSerializer
from menus.models import Menu
import datetime
from menus.simpleMenu import getFoobarMenu


@csrf_exempt
def menu_detail(request, restaurant_name):

    # todo switch restaurant_name

    # menu = getFoobarMenu()

    # test to save stuff to db too
    #dbmenu = Menu(restaurant_id=490051, menu_items_en="potatismus", menu_items_fi="pottumuusi", menu_date="2018-10-03 07:27:28.031091+00")

    date_now = datetime.datetime.today().date()

    try:
        dbmenu = Menu.objects.get(restaurant_id=490051, menu_date=date_now)
    except Menu.DoesNotExist:
        menu = getFoobarMenu()

        menu_items_en = []
        menu_items_fi = []

        for dishoption in menu:
            print(dishoption)
            menu_items_en.append(dishoption["name_en"])
            menu_items_fi.append(dishoption["name_fi"])

        print("menu items en")
        print(menu_items_en)

        dbmenu = Menu(restaurant_id=490051, menu_items_en=menu_items_en, menu_items_fi=menu_items_fi)
        #dbmenu = Menu(restaurant_id=490051, menu_items_en="potatismus", menu_items_fi="pottumuusi")
        #dbmenu.save()

    print("got menu:")
    print(dbmenu)
    # response = HttpResponse(json.dumps(menu), content_type="application/json")
    # response = HttpResponse(json.dumps(menu), content_type="application/json")
    #response = dbmenu.menu_items_fi
    #return HttpResponse(response)
    serializer = MenuSerializer(dbmenu)
    return JsonResponse(serializer.data)


#class Menu(generics.ListCreateAPIView):
#    queryset = Menus.objects.all()
#    serializer_class = TodoSerializer

#    def perform_create(self, serializer):
#        print("saving a new menu item")
#        serializer.save()
