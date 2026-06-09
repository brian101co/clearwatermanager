from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('metrics', '0003_alter_metric_customer'),
        ('payments', '0002_alter_payment_customer'),
        ('manager', '0020_reservation_confirmed_checkout'),
        ('reservations', '0001_initial'),
    ]
    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],  # don't touch the database
            state_operations=[
                migrations.DeleteModel(
                    name='Reservation',
                ),
            ]
        ),
    ]