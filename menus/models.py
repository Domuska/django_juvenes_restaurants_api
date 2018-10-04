from django.db import models

# this model is seriously naive. Implement something real?


class Menu(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    restaurant_id = models.IntegerField(blank=False)
    menu_item_fi = models.TextField()
    menu_item_en = models.TextField()
    menu_date = models.DateField()
    menu_name = models.TextField()

    class Meta:
        # ordering = ('created',)
        app_label = "menus"
