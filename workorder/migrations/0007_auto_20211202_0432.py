# Generated by Django 3.1.12 on 2021-12-02 04:32

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_create_initial_sites'),
        ('workorder', '0006_auto_20211022_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 2, 4, 32, 36, 43641, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='workorder',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workorders', to='sites.site'),
        ),
    ]
