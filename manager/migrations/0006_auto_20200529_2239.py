# Generated by Django 3.0.6 on 2020-05-30 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_customer_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='category',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='description',
        ),
    ]