from rest_framework import serializers
from psycopg2 import Error

from restdecision.models.menu import Menu, MenuItem, MenuVotes
from restdecision.serializers.restaurant import RestaurantSerializer


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = (
            "name",
            "price",
        )


class MenuSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()
    items = MenuItemSerializer(many=True)

    class Meta:
        model = Menu
        fields = "__all__"


class ListMenuVotesSerializer(serializers.Serializer):
    restaurant = serializers.CharField(source="restaurant.name")
    points = serializers.IntegerField(source="count")


class FirstMenuVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuVotes
        fields = ("menu",)

    def validate(self, attrs):
        attrs["points"] = 3
        return attrs

    def create(self, validated_data):
        validated_data["user_id"] = self.context["request"].user.id
        return super(FirstMenuVoteSerializer, self).create(validated_data)


class SecondMenuVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuVotes
        fields = ("menu", "points")

    def create(self, validated_data):
        validated_data["user_id"] = self.context["request"].user.id
        return super(SecondMenuVoteSerializer, self).create(validated_data)


class CreateMenuSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True)
    restaurant_id = serializers.IntegerField()

    class Meta:
        model = Menu
        fields = (
            "restaurant_id",
            "dt_load",
            "items",
        )

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        menu = Menu.objects.create(**validated_data)
        for item in items_data:
            MenuItem.objects.create(menu=menu, **item)
        return menu
