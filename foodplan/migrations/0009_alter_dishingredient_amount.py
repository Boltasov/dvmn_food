# Generated by Django 4.2.5 on 2023-09-27 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan', '0008_alter_dishingredient_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishingredient',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, verbose_name='Количество'),
        ),
    ]
