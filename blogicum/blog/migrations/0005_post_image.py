# Generated by Django 3.2.16 on 2023-08-20 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20230819_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='posts_images', verbose_name='Фото'),
        ),
    ]
