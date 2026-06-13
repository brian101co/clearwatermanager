from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('reservations', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True)),
                ('site', models.CharField(max_length=4)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('canceled', models.BooleanField(default=False)),
                ('res_type', models.PositiveSmallIntegerField(choices=[(1, 'Daily'), (2, 'Weekly'), (3, 'Monthly')], default=1)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservations.reservation')),
            ],
        ),
    ]