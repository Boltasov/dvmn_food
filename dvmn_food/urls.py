from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from foodplan import views

urlpatterns = [
    path('accounts/', include('account.urls')),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('order/', views.order, name='order'),
    path('promo_card/', views.promo_card, name='promo_card'),
    path('confirmation/', views.order_confirmation, name='confirmation'),
    path('menu_created/', views.create_menu, name='menu_created'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
