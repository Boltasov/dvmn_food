import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet


class Allergy(models.Model):
    name = models.CharField(
        max_length=40,
        verbose_name='Название'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Аллергия'
        verbose_name_plural = 'Аллергии'


class Meal(models.Model):
    name = models.CharField(
        max_length=40,
        verbose_name='Название'
    )
    cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Стоимость включения в меню',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Приём пищи'
        verbose_name_plural = 'Приёмы пищи'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=40,
        verbose_name='Название'
    )
    allergy = models.ForeignKey(
        Allergy,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='ingredients',
        verbose_name='Связанная аллергия',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ['name']


class MenuType(models.Model):
    name = models.CharField(
        max_length=40,
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание меню',
        null=True,
        blank=True,
    )
    image = models.ImageField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип меню (диета)'
        verbose_name_plural = 'Типы меню (диеты)'


class Dish(models.Model):
    name = models.CharField(
        max_length=40,
        verbose_name='Название'
    )
    menu_type = models.ManyToManyField(
        MenuType,
        related_name='dishes',
        verbose_name='Тип меню (диета)',
    )
    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE,
        verbose_name='Приём пищи'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='DishIngredient',
        related_name='dishes',
        verbose_name='Ингридиенты'
    )
    image = models.ImageField(
        blank=True,
        verbose_name='Фото блюда',
    )
    preparation = models.TextField(
        verbose_name='Способ приготовления'
    )
    caloricity = models.IntegerField(
        verbose_name='Калорийность',
    )
    promo = models.BooleanField(
        default=False,
        verbose_name='Промо (бесплатный рецепт)'
    )

    def __str__(self):
        return f'{self.name} - {self.meal}'

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'


class DishIngredient(models.Model):
    class Measurement(models.TextChoices):
        UNIT = 'UNIT', 'шт.'
        GRAM = 'GR', 'г.'
        TASTE = 'TASTE', 'по вкусу'
        GLASS = 'GLASS', 'стак.'
        TBLS = 'TBLSP', 'ст. л.'
        TEASP = 'TSP', 'ч. л.'
        LEAF = 'LEAF', 'лист.'
        LITER = 'L', 'л.'
        ML = 'ML', 'мл.'
        ROAST = 'ROAST', 'для обжарки'
        SERVE = 'SERVE', 'для подачи'
        SLICE = 'SLICE', 'ломтика'
        DROPLET = 'DRP', 'капли'
        CLOVE = 'CLOVE', 'зуб.'

    dish = models.ForeignKey(
        Dish,
        verbose_name='Блюдо',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        verbose_name='Количество',
        max_digits=9,
        decimal_places=2,
        blank=True,
        null=True,
    )
    measurement = models.CharField(
        verbose_name='Единица измерения',
        max_length=9,
        blank=True,
        null=True,
        choices=Measurement.choices,
        default=Measurement.TASTE,
    )

    def __str__(self):
        return f'{self.dish} - {self.ingredient}'

    class Meta:
        verbose_name = 'Ингридиент блюда'
        verbose_name_plural = 'Ингридиенты блюда'


class Recommendation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        verbose_name='Блюдо',
    )
    date = models.DateField(
        verbose_name='Дата рекомендации',
    )

    subscription_id = models.IntegerField(
        verbose_name='ID подписки',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.user} - {self.date}: {self.dish}'

    class Meta:
        verbose_name = 'Рекомендация'
        verbose_name_plural = 'Рекомендации'


class PromoCode(models.Model):
    name = models.CharField(
        max_length=40,
        verbose_name='Название',
    )
    percent = models.IntegerField()
    active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return f'{self.name}: скидка {self.percent} процентов'

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'


class UnpaidSubscriptions(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(start_date=None)


class PaidSubscriptions(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(
            start_date__lte=datetime.date.today(),
            end_date__gte=datetime.date.today()
        )


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        db_index=True,
    )
    menu_type = models.ForeignKey(
        MenuType,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Тип меню (диета)',
    )
    months_amount = models.IntegerField(
        verbose_name='Количество месяцев в подписке',
    )
    start_date = models.DateField(
        verbose_name='Дата начала',
        blank=True,
        null=True,
    )
    end_date = models.DateField(
        verbose_name='Дата окончания',
        blank=True,
        null=True,
    )
    meals = models.ManyToManyField(
        Meal,
        related_name='subscriptions',
        verbose_name='Приёмы пищи',
    )
    peoples_amount = models.IntegerField(
        verbose_name='Количество людей',
    )
    allergies = models.ManyToManyField(
        Allergy,
        blank=True,
        related_name='subscriptions',
        verbose_name='Аллергии',
    )
    price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name='Цена'
    )
    promocode = models.ForeignKey(
        PromoCode,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='subscriptions',
        verbose_name='Промокод',
    )

    objects = models.Manager()
    unpaid = UnpaidSubscriptions()
    active = PaidSubscriptions()

    def __str__(self):
        return f'{self.user} - {self.menu_type}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

