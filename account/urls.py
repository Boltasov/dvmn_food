from django.urls import path, include
from .views import profile_view


app_name = 'account'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', profile_view, name='profile'),
]
