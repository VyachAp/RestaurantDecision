from django.contrib.auth.models import User
from django.db import models

from .restaurant import Restaurant


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )
    dt_load = models.DateField("Menu load date", auto_now_add=True)

    class Meta:
        db_table = "menu"
        unique_together = (
            "restaurant",
            "dt_load",
        )


class MenuItem(models.Model):
    name = models.CharField("Position name", max_length=128)
    price = models.DecimalField("Item's price", decimal_places=2, max_digits=8)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items")

    class Meta:
        db_table = "menu_item"


class MenuVotes(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField()

    class Meta:
        db_table = "menu_votes"
        unique_together = (
            "menu",
            "user",
        )
