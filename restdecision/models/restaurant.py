from django.db import models


class Restaurant(models.Model):
    name = models.CharField("Restaurant's name", max_length=64)

    class Meta:
        db_table = "restaurant"
