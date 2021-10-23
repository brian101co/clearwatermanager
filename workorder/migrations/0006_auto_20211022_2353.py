# Generated by Django 3.1.12 on 2021-10-22 23:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc

class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0005_auto_20211021_0500'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='completed_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='workorder',
            name='cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 22, 23, 53, 19, 181591, tzinfo=utc)),
        ),
    ]