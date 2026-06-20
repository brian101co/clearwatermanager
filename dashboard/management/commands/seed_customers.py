from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from reservations.models import Reservation
from metrics.models import Metric  # update 'manager' to your app name if different


class Command(BaseCommand):
    help = 'Seed the database with test customer/reservation data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Metric.objects.all().delete()
        Reservation.objects.all().delete()
        self.stdout.write('Cleared existing customers and metrics...')

        now = timezone.now()

        customers = [
            # --- Active reservations (currently checked in) ---
            {
                "name": "John Smith",
                "site": "12",
                "checkin": now - timedelta(days=2),
                "checkout": now + timedelta(days=3),
                "phone_num": "601-555-0101",
                "info": "Has a large dog. Needs pull-through site.",
                "is_long_term": False,
            },
            {
                "name": "Mary Johnson",
                "site": "14",
                "checkin": now - timedelta(days=1),
                "checkout": now + timedelta(days=5),
                "phone_num": "601-555-0102",
                "info": "",
                "is_long_term": False,
            },
            {
                "name": "Bob Williams",
                "site": "22",
                "checkin": now,
                "checkout": now + timedelta(days=7),
                "phone_num": "601-555-0103",
                "info": "Requests quiet hours after 9pm.",
                "is_long_term": False,
            },

            # --- Checking out soon (within 1-2 days) ---
            {
                "name": "Susan Davis",
                "site": "51",
                "checkin": now - timedelta(days=5),
                "checkout": now + timedelta(days=1),
                "phone_num": "601-555-0104",
                "info": "",
                "is_long_term": False,
            },
            {
                "name": "Tom Martinez",
                "site": "55",
                "checkin": now - timedelta(days=3),
                "checkout": now + timedelta(hours=12),
                "phone_num": "601-555-0105",
                "info": "May extcheckout stay, confirm checkout.",
                "is_long_term": False,
            },

            # --- Checking in soon (arriving in 1-2 days) ---
            {
                "name": "Linda Anderson",
                "site": "60",
                "checkin": now + timedelta(days=1),
                "checkout": now + timedelta(days=6),
                "phone_num": "601-555-0106",
                "info": "",
                "is_long_term": False,
            },
            {
                "name": "James Wilson",
                "site": "64",
                "checkin": now + timedelta(days=2),
                "checkout": now + timedelta(days=9),
                "phone_num": "601-555-0107",
                "info": "Travelling with elderly parent, needs accessible lot.",
                "is_long_term": False,
            },

            # --- Future reservations ---
            {
                "name": "Patricia Moore",
                "site": "75",
                "checkin": now + timedelta(days=7),
                "checkout": now + timedelta(days=14),
                "phone_num": "601-555-0108",
                "info": "",
                "is_long_term": False,
            },
            {
                "name": "Charles Taylor",
                "site": "80",
                "checkin": now + timedelta(days=10),
                "checkout": now + timedelta(days=17),
                "phone_num": "601-555-0109",
                "info": "First time visitor, may need help with hookups.",
                "is_long_term": False,
            },
            {
                "name": "Barbara Thomas",
                "site": "102",
                "checkin": now + timedelta(days=14),
                "checkout": now + timedelta(days=21),
                "phone_num": "601-555-0110",
                "info": "",
                "is_long_term": False,
            },

            # --- Overlap test cases for availability view ---
            {
                "name": "Overlap Test A",
                "site": "5",
                "checkin": now + timedelta(days=3),
                "checkout": now + timedelta(days=8),
                "phone_num": "601-555-0111",
                "info": "Test: overlaps middle of a requested range.",
                "is_long_term": False,
            },
            {
                "name": "Overlap Test B",
                "site": "6",
                "checkin": now + timedelta(days=1),
                "checkout": now + timedelta(days=15),
                "phone_num": "601-555-0112",
                "info": "Test: entirely contains a requested range.",
                "is_long_term": False,
            },
            {
                "name": "Overlap Test C",
                "site": "7",
                "checkin": now - timedelta(days=1),
                "checkout": now + timedelta(days=4),
                "phone_num": "601-555-0113",
                "info": "Test: checkins before and checkouts during a requested range.",
                "is_long_term": False,
            },

            # --- Cabin sites ---
            {
                "name": "Nancy Jackson",
                "site": "10C",
                "checkin": now - timedelta(days=1),
                "checkout": now + timedelta(days=4),
                "phone_num": "601-555-0114",
                "info": "Cabin reservation.",
                "is_long_term": False,
            },
            {
                "name": "Steven White",
                "site": "12C",
                "checkin": now + timedelta(days=5),
                "checkout": now + timedelta(days=10),
                "phone_num": "601-555-0115",
                "info": "Cabin reservation.",
                "is_long_term": False,
            },

            # --- Longterm residents ---
            {
                "name": "Dorothy Harris",
                "site": "116",
                "checkin": now - timedelta(days=60),
                "checkout": now + timedelta(days=300),
                "phone_num": "601-555-0116",
                "info": "Longterm resident. Monthly billing.",
                "is_long_term": True,
            },
            {
                "name": "Donald Clark",
                "site": "118",
                "checkin": now - timedelta(days=90),
                "checkout": now + timedelta(days=270),
                "phone_num": "601-555-0117",
                "info": "Longterm resident. Has two vehicles.",
                "is_long_term": True,
            },
        ]

        created_count = 0
        for data in customers:
            customer = Reservation.objects.create(**data)
            Metric.objects.create(
                customer=customer,
                site=customer.site,
                start=customer.checkin,
                end=customer.checkout,
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded {created_count} customers with associated metrics!'
        ))
        self.stdout.write(self.style.WARNING(
            'Tip: To test availability, search dates between '
            f'{(now + timedelta(days=2)).strftime("%Y-%m-%d")} and '
            f'{(now + timedelta(days=10)).strftime("%Y-%m-%d")} — '
            'sites 5, 6, 7 should be unavailable.'
        ))