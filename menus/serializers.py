from rest_framework import serializers
from menus.models import Menu


class MenuSerializer(serializers.Serializer):

    created = serializers.DateTimeField()
    restaurant_id = serializers.IntegerField(required=True)
    menu_item_fi = serializers.CharField()
    menu_item_en = serializers.CharField()
    menu_date = serializers.DateField()
    menu_name = serializers.CharField()

    def create(self, validated_data):
        print(type(validated_data))
        print(dir(validated_data))
        return Menu.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.menu_item_fi = validated_data.get('menu_item_fi', instance.menu_item_fi)
        instance.menu_item_en = validated_data.get('menu_item_en', instance.menu_item_en)
        instance.menu_date = validated_data.get('menu_date', instance.menu_date)
        instance.menu_name = validated_data.get('menu_name', instance.menu_name)

        instance.save()
        return instance

