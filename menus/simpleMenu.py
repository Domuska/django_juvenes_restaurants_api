from django.http import HttpResponse
from urllib.request import urlopen
import json
import requests

# todo ruokalistojen haku omaan tiedostoonsa, tallenna kantaan
# todo täältä haetaan vain kannasta menu
# todo tee tää ehkä oikein, niinku todoissa tehdään

static_url = "http://juvenes.fi/DesktopModules/Talents.LunchMenu/LunchMenuServices.asmx/GetMenuByWeekday?KitchenId=490051&MenuTypeId=78&Week=40&Weekday=1&lang=%27fi%27&format=json"

# foobar 490051


def respondwithmenu(request, restaurant_name):
    menu = getmenu()
    # print(menu)
    return HttpResponse(menu)


def getmenu():
    response = requests.get(static_url)
    # for some reason Juvenes has all data in the 'd' field
    data_field = json.loads(response.text)
    data_field = json.loads(data_field["d"])

    # print(data_field2["AdditionalName"])

    meals_arr = data_field["MealOptions"]

    # print(meals_arr)

    # todo continue from here
    # remember, fields in meals_arr likely have to be parsed again
    # todo could start to think of writing stuff to DB
    # todo or maybe do route stuff properly
    # todo or maybe fetch food by restaurant properly

    return meals_arr
