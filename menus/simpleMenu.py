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

# https://www.juvenes.fi/foobar
restaurants_dict2 = {
    "foobar": {
        "restaurant_id": 490051,
        "menu_ids": [60, 78, 3, 23, 84]
    },
    "mara": {
        "restaurant_id": 49,
        "menu_ids": [60, 93, 23, 84]
    },
    "väistö": {
        "restaurant_id": 480066,
        "menu_ids": [95, 84]
    },
    "kylymä": {
        "restaurant_id": 490052,
        "menu_ids": [60, 23, 84]
    },
    "napa": {
        "restaurant_id": 480054,
        "menu_ids": [60, 93, 77, 86, 84]
    }
}


def cache_menu(restaurant, date):

    # todo use restaurant id to fetch menu
    # todo date to get restaurant menu
    menu = get_restaurant_menu(restaurant, date)

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


def get_restaurant_menu(restaurant, date):
    """Get all menus for a restaurant for a particular day

    Args:
        restaurant (dictionary): See restaurants_dict2
        date (date): a date object for the day of menus
    Returns:
        array of dictionary items
    """

    restaurant_id = restaurant["restaurant_id"]
    restaurant_menu_ids = restaurant["menu_ids"]

    date_tuple = date.isocalendar()

    # construct urls
    url = juvenes_url_base
    url = add_kitchen_id_to_url(url, restaurant_id)

    url = add_date_to_url(url, date_tuple[1], date_tuple[2])
    # print(url)

    # Get every single menu
    options = []
    for menu_id in restaurant_menu_ids:
        menu_url = add_menu_type_id_to_url(url, menu_id)
        options.extend(get_menu_with_url(menu_url))

    # return as a list of strings
    return options


def get_menu_with_url(url):
    """Get a single Juvenes menu with the URL provided

    Params:
        param url: the URL to use to fetch menu data
    Returns:
        Dictionary with elements name_en, name_fi for dishes
    """

    response = requests.get(url)
    # for some reason Juvenes has all data in the 'd' field
    data_field = json.loads(response.text)
    data_field = json.loads(data_field["d"])

    meals_arr = data_field["MealOptions"]
    # print(meals_arr)

    mealoptions = []

    for mealdata in meals_arr:

        # the restaurants have many different menu items with ids
        # first item of array of options seems to have the actual food,
        # second item might have sauce or somesuch

        for dishitem in mealdata["MenuItems"]:

            mealoptions.append({
                "name_en": dishitem["Name_EN"],
                "name_fi": dishitem["Name_FI"]
            })

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
