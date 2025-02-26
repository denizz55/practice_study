# Generated by Django 5.1.1 on 2025-02-15 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_alter_category_options_alter_report_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='image_after',
            field=models.ImageField(blank=True, null=True, upload_to='reports_after/', verbose_name='Фото после'),
        ),
        migrations.AlterField(
            model_name='report',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='reports/', verbose_name='Фото до'),
        ),
    ]
