from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from workorder.models import WorkOrder  # update app name if different
from sites.models import Site            # update app name if different
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Seed the database with test work order data'

    def handle(self, *args, **kwargs):
        WorkOrder.objects.all().delete()
        self.stdout.write('Cleared existing work orders...')

        # Get the first superuser as the manager
        manager = User.objects.filter(is_superuser=True).first()
        if not manager:
            self.stdout.write(self.style.ERROR('No superuser found. Run createsuperuser first.'))
            return

        now = timezone.now()

        workorders = [
            # --- High Priority / Open ---
            {
                "title": "Electrical hookup not working",
                "site": "12",
                "category": "electrical",
                "priority": 2,
                "description": "Guest reported that the 50amp hookup on Site 12 is not providing power. Breaker has been checked and is not tripped. Needs further inspection by electrician.",
                "estimated_cost": 150.00,
                "cost": None,
                "completed": False,
                "is_recurring": False,
            },
            {
                "title": "Water leak under hookup",
                "site": "22",
                "category": "plumbing",
                "priority": 2,
                "description": "Guest reported a slow water leak at the ground level water hookup. Soil around the connection is saturated. Needs immediate attention to prevent further damage.",
                "estimated_cost": 200.00,
                "cost": None,
                "completed": False,
                "is_recurring": False,
            },
            {
                "title": "Sewer connection cracked",
                "site": "55",
                "category": "plumbing",
                "priority": 2,
                "description": "Sewer connection cap is cracked and causing odor issues. Site has been flagged. New cap and fitting needed.",
                "estimated_cost": 75.00,
                "cost": None,
                "completed": False,
                "is_recurring": False,
            },

            # --- Normal Priority / Open ---
            {
                "title": "Picnic table needs replacing",
                "site": "60",
                "category": "structural",
                "priority": 1,
                "description": "Picnic table on Site 60 has several rotted planks. Two boards have broken through. Table needs full replacement before next guest arrives.",
                "estimated_cost": 120.00,
                "cost": None,
                "completed": False,
                "is_recurring": False,
            },
            {
                "title": "Refrigerator not cooling",
                "site": "10C",
                "category": "appliance",
                "priority": 1,
                "description": "Cabin refrigerator reported not maintaining temperature. Guest moved food to cooler. Technician needs to inspect compressor and coolant levels.",
                "estimated_cost": 250.00,
                "cost": None,
                "completed": False,
                "is_recurring": False,
            },
            {
                "title": "Exterior light out",
                "site": "75",
                "category": "electrical",
                "priority": 1,
                "description": "The exterior site light post on Site 75 is not working. Bulb replacement may resolve the issue but wiring should also be inspected.",
                "estimated_cost": 40.00,
                "cost": None,
                "completed": False,
                "is_recurring": False,
            },
            {
                "title": "Gravel needed on lot",
                "site": "80",
                "category": "structural",
                "priority": 1,
                "description": "Site 80 has developed low spots after recent rain. Gravel needs to be added and graded to improve drainage and parking surface.",
                "estimated_cost": 300.00,
                "cost": None,
                "completed": False,
                "is_recurring": False,
            },

            # --- Low Priority / Open ---
            {
                "title": "Touch up paint on utility box",
                "site": "64",
                "category": "general",
                "priority": 0,
                "description": "The utility box on Site 64 has chipped paint and some surface rust. Needs light sanding and a coat of rust resistant paint.",
                "estimated_cost": 25.00,
                "cost": None,
                "completed": False,
                "is_recurring": False,
            },
            {
                "title": "Trim overgrown bushes",
                "site": "102",
                "category": "landscaping",
                "priority": 0,
                "description": "Bushes along the back of Site 102 have grown into the lot area and are encroaching on the parking pad. Needs trimming back.",
                "estimated_cost": 50.00,
                "cost": None,
                "completed": False,
                "is_recurring": False,
            },

            # --- Recurring Work Orders ---
            {
                "title": "Weekly grounds mowing",
                "site": None,
                "category": "landscaping",
                "priority": 0,
                "description": "Full park grounds mowing including all common areas, road edges, and empty lots. Includes trimming around posts and hookups.",
                "estimated_cost": 150.00,
                "cost": None,
                "completed": False,
                "is_recurring": True,
                "recurring_interval": 7,
            },
            {
                "title": "Monthly pest control inspection",
                "site": None,
                "category": "general",
                "priority": 1,
                "description": "Monthly inspection and treatment for ants, wasps, and other common pests across all cabin sites and common area buildings.",
                "estimated_cost": 200.00,
                "cost": None,
                "completed": False,
                "is_recurring": True,
                "recurring_interval": 30,
            },

            # --- Completed Work Orders ---
            {
                "title": "Replace shower head in cabin",
                "site": "12C",
                "category": "plumbing",
                "priority": 1,
                "description": "Shower head in Cabin 12C was leaking and had low pressure. Replaced with new adjustable shower head.",
                "estimated_cost": 35.00,
                "cost": 28.50,
                "completed": True,
                "completed_at": now - timedelta(days=3),
                "is_recurring": False,
            },
            {
                "title": "Fix gate latch at entrance",
                "site": None,
                "category": "structural",
                "priority": 1,
                "description": "Entrance gate latch was sticking and difficult to open. Lubricated and adjusted the mechanism. Working correctly now.",
                "estimated_cost": 20.00,
                "cost": 15.00,
                "completed": True,
                "completed_at": now - timedelta(days=5),
                "is_recurring": False,
            },
            {
                "title": "Unclog drain at bathhouse",
                "site": None,
                "category": "plumbing",
                "priority": 2,
                "description": "Main drain at the bathhouse was fully clogged causing standing water. Drain snake used to clear blockage. Running freely now.",
                "estimated_cost": 100.00,
                "cost": 85.00,
                "completed": True,
                "completed_at": now - timedelta(days=7),
                "is_recurring": False,
            },
            {
                "title": "Replace broken window screen",
                "site": "10C",
                "category": "structural",
                "priority": 0,
                "description": "Window screen on the front bedroom window of Cabin 10C was torn. Replaced with new screen and re-framed.",
                "estimated_cost": 30.00,
                "cost": 22.00,
                "completed": True,
                "completed_at": now - timedelta(days=10),
                "is_recurring": False,
            },
        ]

        created_count = 0
        for data in workorders:
            site_identifier = data.pop("site")
            site = None
            if site_identifier:
                try:
                    site = Site.objects.get(identifier=site_identifier)
                except Site.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Site {site_identifier} not found, skipping site assignment.'))

            completed_at = data.pop("completed_at", None)

            WorkOrder.objects.create(
                manager=manager,
                site=site,
                completed_at=completed_at,
                **data
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded {created_count} work orders!'
        ))
        self.stdout.write(self.style.WARNING(
            'Note: 3 open high priority, 4 normal, 2 low, 2 recurring, 4 completed.'
        ))