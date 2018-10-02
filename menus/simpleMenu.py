from django.http import HttpResponse
from urllib.request import urlopen
import json
import requests

# todo ruokalistojen haku omaan tiedostoonsa, tallenna kantaan
# todo täältä haetaan vain kannasta menu
# todo tee tää ehkä oikein, niinku todoissa tehdään

#static_url = "http://juvenes.fi/DesktopModules/Talents.LunchMenu/LunchMenuServices.asmx/GetMenuByWeekday?KitchenId=490051&MenuTypeId=78&Week=40&Weekday=1&lang=%27fi%27&format=json"
static_url = "http://juvenes.fi/DesktopModules/Talents.LunchMenu/LunchMenuServices.asmx/GetMenuByWeekday?KitchenId=490051&Week=40&Weekday=1&lang=%27en%27&format=json&MenuTypeId=78&"
juvenes_url_base = "http://juvenes.fi/DesktopModules/Talents.LunchMenu/LunchMenuServices.asmx/GetMenuByWeekday?lang=%27en%27&format=json&"


def respondwithmenu(request, restaurant_name):
    
    # todo switch restaurant_name

    menu = getFoobarMenu()

    response = HttpResponse(json.dumps(menu), content_type="application/json")
    return response


def getFoobarMenu():

    foobar_restaurant_id = 490051
    # todo kato jos nää id:t on samat muissa ravinteleissa
    foobar_menu_ids = [60, 78, 3, 23, 84]

    # foobar 490051
    # menuid 60, 78, 3, 23 84

    # construct urls
    url = juvenes_url_base
    url = add_kitchen_id_to_url(url, foobar_restaurant_id)
    # print(url)
    url = add_date_to_url(url, "40", "1")
    # print(url)

    # Get every single menu
    options = []
    for menu_id in foobar_menu_ids:
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
