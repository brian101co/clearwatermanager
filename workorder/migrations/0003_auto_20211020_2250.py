# Generated by Django 3.1.12 on 2021-10-20 22:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0002_auto_20211018_0146'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 20, 22, 50, 18, 993885)),
        ),
    ]