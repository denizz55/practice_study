from django.contrib import admin
from django.urls import path, include  # Добавляем include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reports.urls')),  # Подключаем маршруты reports
]
