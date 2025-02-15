from django.contrib.auth.models import AbstractUser, User  
from django.db import models
from django.conf import settings

# Кастомная модель пользователя
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",  # исправлено, чтобы не конфликтовало с auth.User.groups
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions_set",  # исправлено
        blank=True
    )

    def __str__(self):
        return self.username

# Категории заявок
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name

class Problem(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
        ('solved', 'Решена'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True, null=True)
    image_before = models.ImageField(upload_to='problems/', blank=True, null=True)
    image_after = models.ImageField(upload_to='problems/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Модель заявки
class Report(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В процессе рассмотрения'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
        ('in_progress', 'В работе'),
        ('resolved', 'Решена'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    image = models.ImageField(upload_to='reports/', null=True, blank=True, verbose_name='Фото до')
    image_after = models.ImageField(upload_to='reports_after/', null=True, blank=True, verbose_name='Фото после')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
