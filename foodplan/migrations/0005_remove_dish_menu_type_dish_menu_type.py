# Generated by Django 4.2.5 on 2023-09-27 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan', '0004_dish_preparation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='menu_type',
        ),
        migrations.AddField(
            model_name='dish',
            name='menu_type',
            field=models.ManyToManyField(related_name='dishes', to='foodplan.menutype', verbose_name='Тип меню (диета)'),
        ),
    ]
