# Generated by Django 4.2 on 2023-08-04 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travelapp', '0009_bookpackage_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookpackage',
            name='city',
        ),
    ]