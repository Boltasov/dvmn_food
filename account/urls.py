from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import profile_view, register


app_name = 'account'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', profile_view, name='profile'),
    path('register/', register, name='register'),
#     path('password-change/',
#          auth_views.PasswordChangeView.as_view(),
#          name='password_change'),
#     path('password_change/done/',
#          auth_views.PasswordChangeDoneView.as_view(),
#          name='password_change_done'),
]
