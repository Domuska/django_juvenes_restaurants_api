# Generated by Django 2.1 on 2018-10-04 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0005_auto_20181003_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='menu_name',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
