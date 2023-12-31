import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from foodplan.models import Subscription, Recommendation


def fetch_weekdays(user, subscr):
    today = datetime.datetime.today()
    week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', ' Воскресенье']
    monday = today - datetime.timedelta(datetime.datetime.weekday(today))
    sunday = today + datetime.timedelta(6 - datetime.datetime.weekday(today))
    recomendations = Recommendation.objects.filter(
        user=user,
        date__gte=monday,
        date__lte=sunday
        ).order_by('date').values('date').distinct()
    print(recomendations)
    for recomendation in recomendations:
        recomendation['day'] = week[datetime.datetime.weekday(recomendation['date'])]
    return recomendations
    

@login_required
def profile_view(request):
    if request.user.is_authenticated == False:
        return redirect('account:login')
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            request.user.set_password(user_form.cleaned_data['password'])
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    test = Subscription.active.all().values_list('user__pk')
    active_subscripts = Subscription.active.filter(user=request.user)
    menues = []
    for subscription in active_subscripts:
        menu = {}
        menu['id'] = subscription.id
        menu['menu'] = subscription.menu_type
        menu['persons'] = subscription.peoples_amount
        menu['allergies'] = subscription.allergies.all()
        menu['meals_count'] = subscription.meals.all().count()
        menu['start_date'] = subscription.start_date
        menu['end_date'] = subscription.end_date
        menu['week'] = fetch_weekdays(request.user, subscription.pk)
        menu['last_date'] = menu['week'].last()['date']
        menues.append(menu)
    
    return render(request, 'lk.html', {'menues': menues,
                                       'user_form': user_form,
                                       'profile_form': profile_form,
                                       })


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect('account:login')
    else:
        user_form = UserRegistrationForm()
        return render(request,
                      'registration.html',
                      {'user_form': user_form})
