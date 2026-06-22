from decimal import Decimal

from django.test import TestCase

from sites.models import Site


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def make_site(**kwargs):
    """
    Create a Site with sensible defaults. Override any field via kwargs.
    lot_id must be unique — callers should pass distinct values when
    creating multiple sites in one test.
    """
    defaults = dict(
        lot_id="TEST-A1",  # "TEST-" prefix never exists in migration data
        info="Test site",
        lot_type="rv",
        under_maintenance=False,
        retired=False,
        water=True,
        electric_30amp=True,
        electric_50amp=False,
        sewer=True,
        wifi=True,
        nightly_rate=Decimal("45.00"),
        weekly_rate=Decimal("280.00"),
        monthly_rate=Decimal("900.00"),
        notes="",
    )
    defaults.update(kwargs)
    return Site.objects.create(**defaults)


# ---------------------------------------------------------------------------
# Base Class
# ---------------------------------------------------------------------------

class SiteTestCase(TestCase):
    """Base class that clears migration-seeded sites before each test class."""
    def setUp(self):
        Site.objects.all().delete()

# ---------------------------------------------------------------------------
# active() / retired
# ---------------------------------------------------------------------------

class ActiveQuerySetTest(SiteTestCase):

    def test_active_includes_non_retired_site(self):
        make_site(lot_id="A1", retired=False)
        self.assertEqual(Site.objects.active().count(), 1)

    def test_active_excludes_retired_site(self):
        make_site(lot_id="A1", retired=True)
        self.assertEqual(Site.objects.active().count(), 0)

    def test_active_returns_only_non_retired_from_mixed_set(self):
        make_site(lot_id="A1", retired=False)
        make_site(lot_id="A2", retired=True)
        make_site(lot_id="A3", retired=False)
        qs = Site.objects.active()
        self.assertEqual(qs.count(), 2)
        self.assertFalse(any(s.retired for s in qs))


# ---------------------------------------------------------------------------
# under_maintenance() / operational()
# ---------------------------------------------------------------------------

class MaintenanceQuerySetTest(SiteTestCase):

    def setUp(self):
        super().setUp()
        self.operational = make_site(lot_id="A1", under_maintenance=False)
        self.maintenance = make_site(lot_id="A2", under_maintenance=True)

    def test_under_maintenance_includes_maintenance_sites(self):
        qs = Site.objects.under_maintenance()
        self.assertIn(self.maintenance, qs)
        self.assertNotIn(self.operational, qs)

    def test_operational_includes_non_maintenance_sites(self):
        qs = Site.objects.operational()
        self.assertIn(self.operational, qs)
        self.assertNotIn(self.maintenance, qs)

    def test_under_maintenance_and_operational_are_mutually_exclusive(self):
        maintenance_count = Site.objects.under_maintenance().count()
        operational_count = Site.objects.operational().count()
        self.assertEqual(maintenance_count + operational_count, Site.objects.count())

    def test_operational_excludes_maintenance_sites(self):
        make_site(lot_id="A3", under_maintenance=True)
        qs = Site.objects.operational()
        self.assertFalse(any(s.under_maintenance for s in qs))


# ---------------------------------------------------------------------------
# available() — active() + operational()
# ---------------------------------------------------------------------------

class AvailableQuerySetTest(SiteTestCase):

    def test_available_includes_active_operational_site(self):
        make_site(lot_id="A1", retired=False, under_maintenance=False)
        self.assertEqual(Site.objects.available().count(), 1)

    def test_available_excludes_retired_site(self):
        make_site(lot_id="A1", retired=True, under_maintenance=False)
        self.assertEqual(Site.objects.available().count(), 0)

    def test_available_excludes_maintenance_site(self):
        make_site(lot_id="A1", retired=False, under_maintenance=True)
        self.assertEqual(Site.objects.available().count(), 0)

    def test_available_excludes_retired_and_maintenance_site(self):
        make_site(lot_id="A1", retired=True, under_maintenance=True)
        self.assertEqual(Site.objects.available().count(), 0)

    def test_available_returns_correct_subset_from_mixed_set(self):
        make_site(lot_id="A1", retired=False, under_maintenance=False)  # available
        make_site(lot_id="A2", retired=True, under_maintenance=False)   # retired
        make_site(lot_id="A3", retired=False, under_maintenance=True)   # maintenance
        make_site(lot_id="A4", retired=True, under_maintenance=True)    # both
        self.assertEqual(Site.objects.available().count(), 1)


# ---------------------------------------------------------------------------
# by_lot_numbers()
# ---------------------------------------------------------------------------

class ByLotNumbersTest(SiteTestCase):

    def setUp(self):
        super().setUp()
        self.a1 = make_site(lot_id="A1")
        self.a2 = make_site(lot_id="A2")
        self.b1 = make_site(lot_id="B1")

    def test_returns_matching_lots(self):
        qs = Site.objects.by_lot_numbers(["A1", "A2"])
        self.assertIn(self.a1, qs)
        self.assertIn(self.a2, qs)
        self.assertNotIn(self.b1, qs)

    def test_returns_empty_for_unknown_lot_numbers(self):
        qs = Site.objects.by_lot_numbers(["Z99", "Z100"])
        self.assertEqual(qs.count(), 0)

    def test_results_ordered_by_lot_id(self):
        qs = Site.objects.by_lot_numbers(["B1", "A1", "A2"])
        lot_ids = list(qs.values_list("lot_id", flat=True))
        self.assertEqual(lot_ids, sorted(lot_ids))

    def test_single_lot_number(self):
        qs = Site.objects.by_lot_numbers(["A1"])
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first().lot_id, "A1")

    def test_empty_list_returns_empty_queryset(self):
        qs = Site.objects.by_lot_numbers([])
        self.assertEqual(qs.count(), 0)


# ---------------------------------------------------------------------------
# by_lot()
# ---------------------------------------------------------------------------

class ByLotTest(SiteTestCase):

    def setUp(self):
        super().setUp()
        self.a1 = make_site(lot_id="A1")
        self.a2 = make_site(lot_id="A2")

    def test_returns_correct_site(self):
        qs = Site.objects.by_lot("A1")
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.a1)

    def test_does_not_return_other_sites(self):
        qs = Site.objects.by_lot("A1")
        self.assertNotIn(self.a2, qs)

    def test_returns_empty_for_unknown_lot(self):
        qs = Site.objects.by_lot("Z99")
        self.assertEqual(qs.count(), 0)


# ---------------------------------------------------------------------------
# calculate_estimated_total()
# ---------------------------------------------------------------------------

class CalculateEstimatedTotalTest(SiteTestCase):
    def setUp(self):
        super().setUp()
        self.site = make_site(
            nightly_rate=Decimal("45.00"),
            weekly_rate=Decimal("280.00"),
            monthly_rate=Decimal("900.00"),
        )

    # --- nightly only ---

    def test_nightly_only_single_day(self):
        total = self.site.calculate_estimated_total(1)
        self.assertEqual(total, Decimal("45.00"))

    def test_nightly_only_multiple_days(self):
        # 6 days — less than a week, no weekly rate applies
        total = self.site.calculate_estimated_total(6)
        self.assertEqual(total, Decimal("270.00"))  # 6 * 45

    # --- weekly rate ---

    def test_exactly_one_week(self):
        # 7 days = 1 week
        total = self.site.calculate_estimated_total(7)
        self.assertEqual(total, Decimal("280.00"))

    def test_one_week_plus_days(self):
        # 9 days = 1 week + 2 days
        total = self.site.calculate_estimated_total(9)
        expected = Decimal("280.00") + (Decimal("45.00") * 2)
        self.assertEqual(total, expected)

    def test_multiple_weeks(self):
        # 14 days = 2 weeks
        total = self.site.calculate_estimated_total(14)
        self.assertEqual(total, Decimal("560.00"))  # 2 * 280

    # --- monthly rate ---

    def test_exactly_one_month(self):
        # 30 days = 1 month
        total = self.site.calculate_estimated_total(30)
        self.assertEqual(total, Decimal("900.00"))

    def test_one_month_plus_days(self):
        # 32 days = 1 month + 2 days
        total = self.site.calculate_estimated_total(32)
        expected = Decimal("900.00") + (Decimal("45.00") * 2)
        self.assertEqual(total, expected)

    def test_one_month_plus_one_week(self):
        # 37 days = 1 month + 1 week
        total = self.site.calculate_estimated_total(37)
        expected = Decimal("900.00") + Decimal("280.00")
        self.assertEqual(total, expected)

    def test_one_month_plus_one_week_plus_days(self):
        # 40 days = 1 month + 1 week + 3 days
        total = self.site.calculate_estimated_total(40)
        expected = Decimal("900.00") + Decimal("280.00") + (Decimal("45.00") * 3)
        self.assertEqual(total, expected)

    def test_multiple_months(self):
        # 60 days = 2 months
        total = self.site.calculate_estimated_total(60)
        self.assertEqual(total, Decimal("1800.00"))

    def test_multiple_months_plus_week_plus_days(self):
        # 72 days = 2 months + 1 week + 5 days
        total = self.site.calculate_estimated_total(72)
        expected = (Decimal("900.00") * 2) + Decimal("280.00") + (Decimal("45.00") * 5)
        self.assertEqual(total, expected)

    # --- fallback to nightly when rates are None ---

    def test_falls_back_to_nightly_when_no_weekly_rate(self):
        site = make_site(
            lot_id="B1",
            nightly_rate=Decimal("45.00"),
            weekly_rate=None,
            monthly_rate=None,
        )
        total = site.calculate_estimated_total(7)
        self.assertEqual(total, Decimal("315.00"))  # 7 * 45

    def test_falls_back_to_nightly_when_no_monthly_rate(self):
        site = make_site(
            lot_id="B2",
            nightly_rate=Decimal("45.00"),
            weekly_rate=Decimal("280.00"),
            monthly_rate=None,
        )
        # Falls back to nightly * duration since total stays 0
        total = site.calculate_estimated_total(30)
        self.assertEqual(total, Decimal("1350.00"))  # 30 * 45

    def test_zero_days_returns_zero(self):
        total = self.site.calculate_estimated_total(0)
        self.assertEqual(total, Decimal("0.00"))

    # --- decimal precision ---

    def test_result_is_decimal_not_float(self):
        total = self.site.calculate_estimated_total(3)
        self.assertIsInstance(total, Decimal)


# ---------------------------------------------------------------------------
# Model fields / defaults
# ---------------------------------------------------------------------------

class SiteModelDefaultsTest(SiteTestCase):
    def test_default_lot_type_is_rv(self):
        site = make_site(lot_id="A1")
        self.assertEqual(site.lot_type, "rv")

    def test_default_under_maintenance_is_false(self):
        site = make_site(lot_id="A1")
        self.assertFalse(site.under_maintenance)

    def test_default_retired_is_false(self):
        site = make_site(lot_id="A1")
        self.assertFalse(site.retired)

    def test_default_amenities(self):
        site = make_site(lot_id="A1")
        self.assertTrue(site.water)
        self.assertTrue(site.electric_30amp)
        self.assertFalse(site.electric_50amp)
        self.assertTrue(site.sewer)
        self.assertTrue(site.wifi)

    def test_lot_id_is_unique(self):
        make_site(lot_id="A1")
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            make_site(lot_id="A1")

    def test_lot_types_choices(self):
        valid_types = [choice[0] for choice in Site.LOT_TYPES]
        self.assertIn("rv", valid_types)
        self.assertIn("cabin", valid_types)
        self.assertIn("tent", valid_types)
        self.assertIn("pullthrough", valid_types)

    def test_get_lot_type_display(self):
        site = make_site(lot_id="A1", lot_type="pullthrough")
        self.assertEqual(site.get_lot_type_display(), "Pull Through")


# ---------------------------------------------------------------------------
# __str__
# ---------------------------------------------------------------------------

class SiteStrTest(SiteTestCase):
    def test_str_returns_lot_id(self):
        site = make_site(lot_id="B12")
        self.assertEqual(str(site), "B12")