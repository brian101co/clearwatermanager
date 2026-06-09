# metrics/migrations/0003_alter_metric_customer.py
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    atomic = False 

    dependencies = [
        ('reservations', '0001_initial'),
        ('metrics', '0002_alter_metric_id'),
    ]
    operations = [
        migrations.AlterField(
            model_name='metric',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservations.reservation'),
        ),
    ]