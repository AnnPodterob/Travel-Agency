# Generated by Django 4.2 on 2023-08-08 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travelapp', '0011_alter_famous_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='famous',
            name='desc',
            field=models.CharField(max_length=2000),
        ),
    ]