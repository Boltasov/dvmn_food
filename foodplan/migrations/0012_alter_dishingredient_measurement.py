# Generated by Django 4.2.5 on 2023-09-27 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan', '0011_alter_dishingredient_measurement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishingredient',
            name='measurement',
            field=models.CharField(choices=[('UNIT', 'шт.'), ('GR', 'г.'), ('TASTE', 'по вкусу'), ('GLASS', 'стак.'), ('TBLSP', 'ст. л.'), ('TSP', 'ч. л.'), ('LEAF', 'лист.'), ('L', 'л.'), ('ML', 'мл.'), ('ROAST', 'для обжарки'), ('SERVE', 'для подачи')], default='TASTE', max_length=9, verbose_name='Единица измерения'),
        ),
    ]
