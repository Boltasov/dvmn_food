from django.contrib import admin

from .models import MenuType, Meal, Allergy, Dish, DishIngredient, \
                    Ingredient, Subscription, Recommendation


admin.site.register(MenuType)
admin.site.register(Meal)
admin.site.register(Allergy)
admin.site.register(Dish)
admin.site.register(DishIngredient)
admin.site.register(Ingredient)
admin.site.register(Subscription)
admin.site.register(Recommendation)
