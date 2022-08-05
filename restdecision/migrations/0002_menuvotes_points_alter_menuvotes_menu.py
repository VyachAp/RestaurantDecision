# Generated by Django 4.1 on 2022-08-04 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("restdecision", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuvotes",
            name="points",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="menuvotes",
            name="menu",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="votes",
                to="restdecision.menu",
            ),
        ),
    ]