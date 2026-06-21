from django.db import migrations


def populate_site_fk(apps, schema_editor):
    Reservation = apps.get_model("reservations", "Reservation")
    Site = apps.get_model("sites", "Site")

    unmatched = []
    for reservation in Reservation.objects.all():
        normalized = reservation.site.strip().upper()
        try:
            site = Site.objects.get(lot_id=normalized)
            reservation.site_fk = site
            reservation.save(update_fields=["site_fk"])
        except Site.DoesNotExist:
            unmatched.append((reservation.id, reservation.site))

    if unmatched:
        print(f"\n⚠️  {len(unmatched)} reservations could not be matched to a Site:")
        for res_id, site_val in unmatched:
            print(f"   Reservation id={res_id}, site value='{site_val}'")


def reverse_populate(apps, schema_editor):
    Reservation = apps.get_model("reservations", "Reservation")
    Reservation.objects.update(site_fk=None)


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0005_reservation_site_fk"), 
    ]

    operations = [
        migrations.RunPython(populate_site_fk, reverse_populate),
    ]