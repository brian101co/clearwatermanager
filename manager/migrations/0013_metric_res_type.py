# Generated by Django 3.1.12 on 2021-10-16 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0012_customers_to_metrics'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='res_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Daily'), (2, 'Weekly'), (3, 'Monthly'), (4, 'Unknown')], default=4),
        ),
    ]
