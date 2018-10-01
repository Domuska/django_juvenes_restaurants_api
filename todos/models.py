from django.db import models


class Todos(models.Model):
    title = models.CharField(max_length=500)
    completed = models.BooleanField(default=False)
    order = models.IntegerField(db_column='position', default=0)


class Mythings(models.Model):
    thing = models.CharField(max_length=20)
    anInteger = models.IntegerField(default=1)
