from django.db import models

# this model is seriously naive. Implement something real?


class Menu(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    restaurant_id = models.IntegerField(blank=False)
    menu_items_fi = models.TextField()
    menu_items_en = models.TextField()
    menu_date = models.DateField(null=True)

    class Meta:
        # ordering = ('created',)
        app_label = "menus"
