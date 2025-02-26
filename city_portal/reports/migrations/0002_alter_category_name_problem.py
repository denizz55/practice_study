# Generated by Django 5.1.1 on 2025-02-14 22:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'На рассмотрении'), ('approved', 'Одобрена'), ('rejected', 'Отклонена'), ('solved', 'Решена')], default='pending', max_length=20)),
                ('rejection_reason', models.TextField(blank=True, null=True)),
                ('image_before', models.ImageField(blank=True, null=True, upload_to='problems/')),
                ('image_after', models.ImageField(blank=True, null=True, upload_to='problems/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
