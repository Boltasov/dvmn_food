from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from foodplan import views

urlpatterns = [
    path('account/', include('account.urls')),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
