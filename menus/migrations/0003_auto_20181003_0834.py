# Generated by Django 2.1 on 2018-10-03 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0002_auto_20181003_0731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='menu_date',
            field=models.DateTimeField(null=True),
        ),
    ]
