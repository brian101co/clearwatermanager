from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('site', models.CharField(max_length=4)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('phoneNum', models.CharField(max_length=25)),
                ('info', models.TextField(blank=True)),
                ('is_long_term', models.BooleanField(default=False)),
                ('confirmed_checkout', models.BooleanField(default=False)),
            ],
        ),
    ]