# Generated by Django 3.1.12 on 2021-10-11 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0007_auto_20200530_1933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='title',
        ),
    ]
