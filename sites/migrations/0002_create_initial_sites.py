# Generated by Django 3.1.12 on 2021-10-20 01:48

from django.db import migrations


def create_initial_sites(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')

    sites = Site.objects.all()
    all_sites = ["122", "120", "118", "116", "114", "112", "110", "108", "106", "104", "102", "19", "17", "15", "13", "11",
                "9", "7", "5", "6", "8", "10", "12", "14", "10C", "12C", "14C", "16", "18", "20", "22", "24", "26", "28",
                "30", "85", "51", "53", "55", "57", "59", "65", "67", "69", "73", "75", "77", "79", "81", "83", "82", "80",
                "78", "76", "74", "72", "70", "68", "66", "64", "62", "60", "58", "56", "63"]
    for site in sites:
        if site.identifier in all_sites:
            all_sites.remove(site.identifier)
    
    for site in all_sites:
        new_site = Site(identifier=site, info="No information available.")
        new_site.save()

class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_sites),
    ]
