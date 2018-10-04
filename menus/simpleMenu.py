from django.http import HttpResponse
from urllib.request import urlopen
from menus.serializers import MenuSerializer
from menus.models import Menu
import json
import requests
import datetime

# http://www.django-rest-framework.org/tutorial/1-serialization/

# https://www.juvenes.fi/foobar
juvenes_url_base = "http://juvenes.fi/DesktopModules/Talents.LunchMenu/LunchMenuServices.asmx/" \
                   "GetMenuByWeekday?lang=%27en%27&format=json&"

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
    # call networking functions to fetch restaurant data
    # save that to db

    menu = get_restaurant_menu(restaurant, date)

    for dishoption in menu:
        # print(dishoption)
        dish = Menu(
            restaurant_id=restaurant["restaurant_id"],
            menu_item_en=dishoption["meal_name_en"],
            menu_item_fi=dishoption["meal_name_fi"],
            menu_date=date,
            menu_name=dishoption["menu_name"]
        )
        dish.save()


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
    """Get a single Juvenes menu with the URL provided over the network

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
    print(meals_arr)

    mealoptions = []

    for mealdata in meals_arr:

        # first item of array of options seems to have the actual food,
        # second item might have sauce or somesuch

        meal_option_dict = {
            "meal_name_en": "",
            "meal_name_fi": "",
            "menu_name": mealdata["Name"]
        }

        for enumer_value, dish_item in enumerate(mealdata["MenuItems"]):
            if enumer_value:
                meal_option_dict["meal_name_en"] += ", "
                meal_option_dict["meal_name_fi"] += ", "

            meal_option_dict["meal_name_en"] += dish_item["Name_EN"]
            meal_option_dict["meal_name_fi"] += dish_item["Name_FI"]

        mealoptions.append(meal_option_dict)

    # print(mealoptions)

    return mealoptions


def add_kitchen_id_to_url(url, kitchen_id):
    return url + "KitchenId=%s&" % kitchen_id


def add_menu_type_id_to_url(url, menu_type_id):
    return url + "MenuTypeId=%s&" % menu_type_id


def add_date_to_url(url, weeknumber, weekdaynumber):
    url = url + "Weekday=%s&" % weekdaynumber
    url = url + "Week=%s&" % weeknumber
    return url

