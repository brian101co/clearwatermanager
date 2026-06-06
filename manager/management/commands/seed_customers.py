from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from manager.models import Customer


class Command(BaseCommand):
    help = 'Seed the database with test customer/reservation data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Customer.objects.all().delete()
        self.stdout.write('Cleared existing customers...')

        now = timezone.now()

        customers = [
            # --- Active reservations (currently checked in) ---
            {
                "name": "John Smith",
                "site": "12",
                "start": now - timedelta(days=2),
                "end": now + timedelta(days=3),
                "phoneNum": "601-555-0101",
                "info": "Has a large dog. Needs pull-through site."
            },
            {
                "name": "Mary Johnson",
                "site": "14",
                "start": now - timedelta(days=1),
                "end": now + timedelta(days=5),
                "phoneNum": "601-555-0102",
                "info": ""
            },
            {
                "name": "Bob Williams",
                "site": "22",
                "start": now,
                "end": now + timedelta(days=7),
                "phoneNum": "601-555-0103",
                "info": "Requests quiet hours after 9pm."
            },

            # --- Checking out soon (within 1-2 days) ---
            {
                "name": "Susan Davis",
                "site": "51",
                "start": now - timedelta(days=5),
                "end": now + timedelta(days=1),
                "phoneNum": "601-555-0104",
                "info": ""
            },
            {
                "name": "Tom Martinez",
                "site": "55",
                "start": now - timedelta(days=3),
                "end": now + timedelta(hours=12),
                "phoneNum": "601-555-0105",
                "info": "May extend stay, confirm checkout."
            },

            # --- Checking in soon (arriving in 1-2 days) ---
            {
                "name": "Linda Anderson",
                "site": "60",
                "start": now + timedelta(days=1),
                "end": now + timedelta(days=6),
                "phoneNum": "601-555-0106",
                "info": ""
            },
            {
                "name": "James Wilson",
                "site": "64",
                "start": now + timedelta(days=2),
                "end": now + timedelta(days=9),
                "phoneNum": "601-555-0107",
                "info": "Travelling with elderly parent, needs accessible lot."
            },

            # --- Future reservations ---
            {
                "name": "Patricia Moore",
                "site": "75",
                "start": now + timedelta(days=7),
                "end": now + timedelta(days=14),
                "phoneNum": "601-555-0108",
                "info": ""
            },
            {
                "name": "Charles Taylor",
                "site": "80",
                "start": now + timedelta(days=10),
                "end": now + timedelta(days=17),
                "phoneNum": "601-555-0109",
                "info": "First time visitor, may need help with hookups."
            },
            {
                "name": "Barbara Thomas",
                "site": "102",
                "start": now + timedelta(days=14),
                "end": now + timedelta(days=21),
                "phoneNum": "601-555-0110",
                "info": ""
            },

            # --- Overlap test cases for availability view ---
            {
                "name": "Overlap Test A",
                "site": "5",
                "start": now + timedelta(days=3),
                "end": now + timedelta(days=8),
                "phoneNum": "601-555-0111",
                "info": "Test: overlaps middle of a requested range."
            },
            {
                "name": "Overlap Test B",
                "site": "6",
                "start": now + timedelta(days=1),
                "end": now + timedelta(days=15),
                "phoneNum": "601-555-0112",
                "info": "Test: entirely contains a requested range."
            },
            {
                "name": "Overlap Test C",
                "site": "7",
                "start": now - timedelta(days=1),
                "end": now + timedelta(days=4),
                "phoneNum": "601-555-0113",
                "info": "Test: starts before and ends during a requested range."
            },

            # --- Cabin sites ---
            {
                "name": "Nancy Jackson",
                "site": "10C",
                "start": now - timedelta(days=1),
                "end": now + timedelta(days=4),
                "phoneNum": "601-555-0114",
                "info": "Cabin reservation."
            },
            {
                "name": "Steven White",
                "site": "12C",
                "start": now + timedelta(days=5),
                "end": now + timedelta(days=10),
                "phoneNum": "601-555-0115",
                "info": "Cabin reservation."
            },

            # --- Longterm residents ---
            {
                "name": "Dorothy Harris",
                "site": "116",
                "start": now - timedelta(days=60),
                "end": now + timedelta(days=300),
                "phoneNum": "601-555-0116",
                "info": "Longterm resident. Monthly billing."
            },
            {
                "name": "Donald Clark",
                "site": "118",
                "start": now - timedelta(days=90),
                "end": now + timedelta(days=270),
                "phoneNum": "601-555-0117",
                "info": "Longterm resident. Has two vehicles."
            },
        ]

        for data in customers:
            Customer.objects.create(**data)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded {len(customers)} customers!'
        ))
        self.stdout.write(self.style.WARNING(
            'Tip: To test availability, search dates between '
            f'{(now + timedelta(days=2)).strftime("%Y-%m-%d")} and '
            f'{(now + timedelta(days=10)).strftime("%Y-%m-%d")} — '
            'sites 5, 6, 7 should be unavailable.'
        ))