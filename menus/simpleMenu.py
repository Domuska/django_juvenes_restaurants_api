from django.http import HttpResponse
from urllib.request import urlopen
from menus.serializers import MenuSerializer
from menus.models import Menu
import json
import requests
import datetime

# todo ruokalistojen haku omaan tiedostoonsa, tallenna kantaan
# todo täältä haetaan vain kannasta menu
# todo tee tää ehkä oikein, niinku todoissa tehdään

# http://www.django-rest-framework.org/tutorial/1-serialization/

# static_url = "http://juvenes.fi/DesktopModules/Talents.LunchMenu/LunchMenuServices.asmx/GetMenuByWeekday?KitchenId=490051&Week=40&Weekday=1&lang=%27en%27&format=json&MenuTypeId=78&"
juvenes_url_base = "http://juvenes.fi/DesktopModules/Talents.LunchMenu/LunchMenuServices.asmx/GetMenuByWeekday?lang=%27en%27&format=json&"


restaurants_dict2 = {
    "foobar": {
        "restaurant_id": 490051,
        "menu_ids": [60, 78, 3, 23, 84]
    },
    "mara": {
        "restaurant_id": 49,
        "menu_ids": [60, 93, 23, 84]
    }
}


def cache_menu(restaurant, date):

    # todo use restaurant id to fetch menu
    # todo date to get restaurant menu
    menu = get_restaurant_menu(restaurant)

    for dishoption in menu:
        print(dishoption)
        dish = Menu(
            restaurant_id=restaurant["restaurant_id"],
            menu_item_en=dishoption["name_en"],
            menu_item_fi=dishoption["name_fi"],
            menu_date=date
        )
        dish.save()
        #menu_items_en.append(dishoption["name_en"])
        #menu_items_fi.append(dishoption["name_fi"])

    #print("menu items en")
    #print(menu_items_en)

    #dbmenu = Menu(
    #    restaurant_id=490051,
    #    menu_item_en=menu_items_en,
    #    menu_item_fi=menu_items_fi,
    #    menu_date=date
    #)
    #dbmenu.save()
    #return dbmenu





def respondwithmenu(request, restaurant_name):


    date_now = datetime.datetime.today().date()

    try:
        dbmenu = Menu.objects.get(restaurant_id=490051, menu_date=date_now)
    except Menu.DoesNotExist:

        menu = get_restaurant_menu()

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
    response = dbmenu.menu_items_fi
    return HttpResponse("this should not come back from here any more")


def get_restaurant_menu(restaurant):

    # https://www.juvenes.fi/foobar

    restaurant_id = restaurant["restaurant_id"]
    # todo kato jos nää id:t on samat muissa ravinteleissa
    restaurant_menu_ids = restaurant["menu_ids"]

    # foobar 490051
    # menuid 60, 78, 3, 23 84

    # construct urls
    url = juvenes_url_base
    url = add_kitchen_id_to_url(url, restaurant_id)
    # print(url)
    url = add_date_to_url(url, "40", "1")
    # print(url)

    # Get every single menu
    options = []
    for menu_id in restaurant_menu_ids:
        menu_url = add_menu_type_id_to_url(url, menu_id)
        options.extend(get_menu_with_url(menu_url))

    # return as a list of strings
    return options


def get_menu_with_url(url):
    response = requests.get(url)
    # for some reason Juvenes has all data in the 'd' field
    data_field = json.loads(response.text)
    data_field = json.loads(data_field["d"])

    meals_arr = data_field["MealOptions"]
    # print(meals_arr)

    mealoptions = []
    mealoptionsdict = {
        "options": []
    }

    for mealdata in meals_arr:

        # the restaurants have many different menu items with ids
        # first item of array of options seems to have the actual food,
        # second item might have sauce or somesuch

        for dishitem in mealdata["MenuItems"]:

            mealoptions.append({
                "name_en": dishitem["Name_EN"],
                "name_fi": dishitem["Name_FI"]
            })

            # mealoptionsdict["options"].append({
            #    "name_en": dishitem["Name_EN"],
            #    "name_fi": dishitem["Name_FI"]
            # })

        # dish = item[0]["Name"]
        # print(dish)
        # mealoptions.append(dish)

    # todo continue from here
    # todo could start to think of writing stuff to DB
    # todo or maybe do route stuff properly

    print(mealoptions)

    return mealoptions


def add_kitchen_id_to_url(url, kitchen_id):
    #KitchenId=490051&
    return url + "KitchenId=%s&" % kitchen_id


def add_menu_type_id_to_url(url, menu_type_id):
    return url + "MenuTypeId=%s&" % menu_type_id


def add_date_to_url(url, weeknumber, weekdaynumber):
    url = url + "Weekday=%s&" % weekdaynumber
    url = url + "Week=%s&" % weeknumber
    return url


# def add_lang_to_url(url, langcode):
#    return url + "lang=%27fi%27"
