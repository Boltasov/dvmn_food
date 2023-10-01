from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Model
import random
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


from .models import MenuType, Allergy, Meal, Subscription, Dish, Recommendation


def calculate_cost(meals, term):
    one_month_cost = 0
    for meal in meals:
        one_month_cost += meal.cost
    if term == '1':
        factor = 1
    elif term == '3':
        factor = 1.9
    elif term == '6':
        factor = 1.8
    else:
        factor = 1.7
    cost = round(one_month_cost * Decimal(factor))
    return cost


def index(request):
    context = {
        'is_index_page': True,
    }
    return render(request, 'index.html', context)

def order(request):
    if request.user.is_authenticated == False:
        return redirect('account:login')
    menu_types = MenuType.objects.all()
    allergies = Allergy.objects.all()
    meals = Meal.objects.all()
    return render(request, 'order.html', {
        'menu_types': menu_types,
        'allergies': allergies,
        'meals': meals,
    })


def order_confirmation(request):
    foodtype = request.GET.get('foodtype')
    if not foodtype:
        return render(request, 'order_confirmation.html', {})
    persons_count = int(request.GET.get('persons_count'))
    selected_menu = get_object_or_404(MenuType, pk=foodtype)
    term = request.GET.get('term')
    meals = Meal.objects.all()
    selected_meals = []
    for meal in meals:
        param = 'meal' + str(meal.pk)
        if request.GET.get(param) != '0':
            selected_meals.append(meal)
    allergies = Allergy.objects.all()
    selected_allergies = []
    for allergy in allergies:
        param = 'allergy' + str(allergy.pk)
        if request.GET.get(param) != None:
            selected_allergies.append(allergy)
    cost = calculate_cost(selected_meals, term)
    try:
        order = Subscription.unpaid.filter(user=request.user)[0]
    except IndexError:
        order = Subscription(user=request.user)
    order.menu_type = selected_menu
    order.months_amount = term
    order.peoples_amount = persons_count
    order.price = cost
    order.save()
    for meal in selected_meals:
        order.meals.add(meal)
    for allergy in selected_allergies:
        order.allergies.add(allergy)
    order.save()
    request.session['order_id'] = order.id
    for meal in order.meals.all():
        print(meal)
    return render(request, 'order_confirmation.html', {
        'menu': selected_menu,
        'term': term,
        'meals': selected_meals,
        'allergies': selected_allergies,
        'cost': cost,
        'persons_count': persons_count,
    })

def promo_card(request):
    dish = Dish.objects.filter(promo=True).order_by('?').first()
    dish_ingredients = dish.dishingredient_set.all()
    context = {
        'dish': dish,
        'dish_ingredients': dish_ingredients,
    }
    return render(request, 'promo_card.html', context)


def create_menu(request):
    user = request.user
    order_id = request.session.get('order_id')
    current_date = date.today()
    order = Subscription.objects.get(id=order_id)
    recommendations = Recommendation.objects.filter(subscription_id=order_id)
    if not recommendations.exists():
        end_date = current_date + relativedelta(months=order.months_amount)
        dishes = Dish.objects.filter(menu_type=order.menu_type)
        for allergy in order.allergies.all():
            dishes = dishes.exclude(ingredients__allergy=allergy)

        while current_date <= end_date:
            for meal in Meal.objects.all():
                available_dishes = dishes.filter(meal=meal)
                if available_dishes.exists():
                    selected_dish = random.choice(available_dishes)

                    recommendation = Recommendation(user=user, dish=selected_dish, date=current_date, subscription_id=order_id)
                    recommendation.save()
            current_date += timedelta(days=1)
        order.start_date = current_date
        order.end_date = end_date
        order.save()
    context = {
        'menu_type': order.menu_type,
    }
    return render(request, 'menu_created.html', context)

