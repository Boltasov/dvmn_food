# Generated by Django 4.2.5 on 2023-09-27 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan', '0003_meal_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='preparation',
            field=models.TextField(default='', verbose_name='Способ приготовления'),
            preserve_default=False,
        ),
    ]
