from django.db import migrations, models


def rename_table_forward(apps, schema_editor):
    schema_editor.connection.disable_constraint_checking()

    if schema_editor.connection.vendor == 'sqlite':
        # Rename reservation table
        schema_editor.execute('ALTER TABLE manager_reservation RENAME TO reservations_reservation;')

        # Recreate metrics_metric with updated FK
        schema_editor.execute("""
            CREATE TABLE "metrics_metric_new" (
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "site" varchar(4) NOT NULL,
                "start" datetime NOT NULL,
                "end" datetime NOT NULL,
                "canceled" bool NOT NULL,
                "res_type" smallint unsigned NOT NULL CHECK ("res_type" >= 0),
                "customer_id" bigint NULL REFERENCES "reservations_reservation" ("id") DEFERRABLE INITIALLY DEFERRED
            );
        """)
        schema_editor.execute("INSERT INTO metrics_metric_new SELECT * FROM metrics_metric;")
        schema_editor.execute("DROP TABLE metrics_metric;")
        schema_editor.execute("ALTER TABLE metrics_metric_new RENAME TO metrics_metric;")

        # Recreate payments_payment with updated FK
        schema_editor.execute("""
            CREATE TABLE "payments_payment_new" (
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "amount_due" decimal NOT NULL,
                "amount_paid" decimal NOT NULL,
                "status" varchar(10) NOT NULL,
                "method" varchar(10) NULL,
                "notes" text NOT NULL,
                "created_at" datetime NOT NULL,
                "paid_at" datetime NULL,
                "customer_id" bigint NOT NULL REFERENCES "reservations_reservation" ("id") DEFERRABLE INITIALLY DEFERRED
            );
        """)
        schema_editor.execute("INSERT INTO payments_payment_new SELECT * FROM payments_payment;")
        schema_editor.execute("DROP TABLE payments_payment;")
        schema_editor.execute("ALTER TABLE payments_payment_new RENAME TO payments_payment;")

    elif schema_editor.connection.vendor == 'mysql':
        schema_editor.execute("RENAME TABLE manager_reservation TO reservations_reservation;")

    schema_editor.connection.enable_constraint_checking()


def rename_table_reverse(apps, schema_editor):
    schema_editor.connection.disable_constraint_checking()

    if schema_editor.connection.vendor == 'sqlite':
        # Rename reservation table back
        schema_editor.execute('ALTER TABLE reservations_reservation RENAME TO manager_reservation;')

        # Recreate metrics_metric with original FK
        schema_editor.execute("""
            CREATE TABLE "metrics_metric_new" (
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "site" varchar(4) NOT NULL,
                "start" datetime NOT NULL,
                "end" datetime NOT NULL,
                "canceled" bool NOT NULL,
                "res_type" smallint unsigned NOT NULL CHECK ("res_type" >= 0),
                "customer_id" bigint NULL REFERENCES "manager_reservation" ("id") DEFERRABLE INITIALLY DEFERRED
            );
        """)
        schema_editor.execute("INSERT INTO metrics_metric_new SELECT * FROM metrics_metric;")
        schema_editor.execute("DROP TABLE metrics_metric;")
        schema_editor.execute("ALTER TABLE metrics_metric_new RENAME TO metrics_metric;")

        # Recreate payments_payment with original FK
        schema_editor.execute("""
            CREATE TABLE "payments_payment_new" (
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "amount_due" decimal NOT NULL,
                "amount_paid" decimal NOT NULL,
                "status" varchar(10) NOT NULL,
                "method" varchar(10) NULL,
                "notes" text NOT NULL,
                "created_at" datetime NOT NULL,
                "paid_at" datetime NULL,
                "customer_id" bigint NOT NULL REFERENCES "manager_reservation" ("id") DEFERRABLE INITIALLY DEFERRED
            );
        """)
        schema_editor.execute("INSERT INTO payments_payment_new SELECT * FROM payments_payment;")
        schema_editor.execute("DROP TABLE payments_payment;")
        schema_editor.execute("ALTER TABLE payments_payment_new RENAME TO payments_payment;")

    elif schema_editor.connection.vendor == 'mysql':
        schema_editor.execute("RENAME TABLE reservations_reservation TO manager_reservation;")

    schema_editor.connection.enable_constraint_checking()


class Migration(migrations.Migration):
    initial = True
    atomic = False

    dependencies = [
       
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(
                    rename_table_forward,
                    rename_table_reverse
                ),
            ],
            state_operations=[
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
        ),
    ]