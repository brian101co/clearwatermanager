# Generated by Django 3.0.6 on 2020-05-30 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_auto_20200529_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='description',
            field=models.TextField(default='description'),
            preserve_default=False,
        ),
    ]