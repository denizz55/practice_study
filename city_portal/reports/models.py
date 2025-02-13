from django.db import models
from django.contrib.auth.models import User

# Категории проблем
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Заявки пользователей
class Report(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('resolved', 'Решена'),
        ('rejected', 'Отклонена'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем
    title = models.CharField(max_length=200)  # Название проблемы
    description = models.TextField()  # Описание
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)  # Категория
    image = models.ImageField(upload_to='reports/', blank=True, null=True)  # Фото
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')  # Статус
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return self.title
