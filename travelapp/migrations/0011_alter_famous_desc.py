# Generated by Django 4.2 on 2023-08-08 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travelapp', '0010_remove_bookpackage_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='famous',
            name='desc',
            field=models.CharField(max_length=1000),
        ),
    ]
