# Generated by Django 4.1.7 on 2023-03-30 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Slug'),
        ),
    ]
