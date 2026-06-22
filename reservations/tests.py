from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from sites.models import Site
from reservations.models import Reservation


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_site(**kwargs):
    defaults = dict(lot_id="A1", lot_type="RV", retired=False, under_maintenance=False)
    defaults.update(kwargs)
    return Site.objects.create(**defaults)


def make_reservation(site, checkin_offset=0, checkout_offset=3, **kwargs):
    """
    Create a Reservation relative to today.
    checkin_offset / checkout_offset are days from now.
    """
    now = timezone.now()
    defaults = dict(
        name="Test Guest",
        site=site,
        checkin=now + timedelta(days=checkin_offset),
        checkout=now + timedelta(days=checkout_offset),
        phone_num="555-0100",
        is_long_term=False,
        confirmed_checkout=False,
    )
    defaults.update(kwargs)
    return Reservation.objects.create(**defaults)


# ---------------------------------------------------------------------------
# active() / checked_out()
# ---------------------------------------------------------------------------

class ActiveQuerySetTest(TestCase):
    def setUp(self):
        self.site = make_site()

    def test_active_includes_unconfirmed_checkout(self):
        make_reservation(self.site, confirmed_checkout=False)
        self.assertEqual(Reservation.objects.active().count(), 1)

    def test_active_excludes_confirmed_checkout(self):
        make_reservation(self.site, confirmed_checkout=True)
        self.assertEqual(Reservation.objects.active().count(), 0)

    def test_checked_out_includes_confirmed_checkout(self):
        make_reservation(self.site, confirmed_checkout=True)
        self.assertEqual(Reservation.objects.checked_out().count(), 1)

    def test_checked_out_excludes_unconfirmed_checkout(self):
        make_reservation(self.site, confirmed_checkout=False)
        self.assertEqual(Reservation.objects.checked_out().count(), 0)

    def test_active_and_checked_out_are_mutually_exclusive(self):
        make_reservation(self.site, confirmed_checkout=False)
        make_reservation(self.site, confirmed_checkout=True)
        self.assertEqual(Reservation.objects.active().count(), 1)
        self.assertEqual(Reservation.objects.checked_out().count(), 1)
        self.assertEqual(Reservation.objects.count(), 2)


# ---------------------------------------------------------------------------
# short_term() / long_term()
# ---------------------------------------------------------------------------

class TermTypeQuerySetTest(TestCase):
    def setUp(self):
        self.site = make_site()
        self.short = make_reservation(self.site, is_long_term=False)
        self.long = make_reservation(self.site, checkin_offset=5, checkout_offset=35, is_long_term=True)

    def test_short_term_excludes_long_term(self):
        qs = Reservation.objects.get_queryset().short_term()
        self.assertIn(self.short, qs)
        self.assertNotIn(self.long, qs)

    def test_long_term_excludes_short_term(self):
        qs = Reservation.objects.get_queryset().long_term()
        self.assertIn(self.long, qs)
        self.assertNotIn(self.short, qs)

    def test_short_and_long_term_cover_all_reservations(self):
        short_count = Reservation.objects.get_queryset().short_term().count()
        long_count = Reservation.objects.get_queryset().long_term().count()
        self.assertEqual(short_count + long_count, Reservation.objects.count())


# ---------------------------------------------------------------------------
# get_by_site()
# ---------------------------------------------------------------------------

class GetBySiteTest(TestCase):
    def setUp(self):
        self.site_a = make_site(lot_id="A1")
        self.site_b = make_site(lot_id="B1")
        self.res_a = make_reservation(self.site_a)
        self.res_b = make_reservation(self.site_b)

    def test_returns_reservations_for_correct_site(self):
        qs = Reservation.objects.get_queryset().get_by_site("A1")
        self.assertIn(self.res_a, qs)
        self.assertNotIn(self.res_b, qs)

    def test_returns_empty_for_unknown_site(self):
        qs = Reservation.objects.get_queryset().get_by_site("Z99")
        self.assertEqual(qs.count(), 0)


# ---------------------------------------------------------------------------
# checking_in_on() / checking_out_on()
# ---------------------------------------------------------------------------

class CheckInOutOnTest(TestCase):
    def setUp(self):
        self.site = make_site()
        self.today = timezone.now().date()

    def test_checking_in_on_today(self):
        make_reservation(self.site, checkin_offset=0, checkout_offset=3)
        qs = Reservation.objects.get_queryset().checking_in_on(self.today)
        self.assertEqual(qs.count(), 1)

    def test_checking_in_on_excludes_other_dates(self):
        make_reservation(self.site, checkin_offset=1, checkout_offset=4)
        qs = Reservation.objects.get_queryset().checking_in_on(self.today)
        self.assertEqual(qs.count(), 0)

    def test_checking_out_on_today(self):
        make_reservation(self.site, checkin_offset=-3, checkout_offset=0)
        qs = Reservation.objects.get_queryset().checking_out_on(self.today)
        self.assertEqual(qs.count(), 1)

    def test_checking_out_on_excludes_other_dates(self):
        make_reservation(self.site, checkin_offset=-3, checkout_offset=-1)
        qs = Reservation.objects.get_queryset().checking_out_on(self.today)
        self.assertEqual(qs.count(), 0)

    def test_checking_in_excludes_long_term(self):
        make_reservation(self.site, checkin_offset=0, checkout_offset=30, is_long_term=True)
        qs = Reservation.objects.get_queryset().checking_in_on(self.today)
        self.assertEqual(qs.count(), 0)

    def test_checking_out_excludes_long_term(self):
        make_reservation(self.site, checkin_offset=-30, checkout_offset=0, is_long_term=True)
        qs = Reservation.objects.get_queryset().checking_out_on(self.today)
        self.assertEqual(qs.count(), 0)


# ---------------------------------------------------------------------------
# overdue() / overdue_leases_on()
# ---------------------------------------------------------------------------

class OverdueTest(TestCase):
    def setUp(self):
        self.site = make_site()
        self.today = timezone.now().date()

    def test_overdue_includes_past_checkout_short_term(self):
        make_reservation(self.site, checkin_offset=-5, checkout_offset=-1)
        qs = Reservation.objects.get_queryset().overdue(self.today)
        self.assertEqual(qs.count(), 1)

    def test_overdue_excludes_future_checkout(self):
        make_reservation(self.site, checkin_offset=0, checkout_offset=3)
        qs = Reservation.objects.get_queryset().overdue(self.today)
        self.assertEqual(qs.count(), 0)

    def test_overdue_excludes_long_term(self):
        make_reservation(self.site, checkin_offset=-35, checkout_offset=-1, is_long_term=True)
        qs = Reservation.objects.get_queryset().overdue(self.today)
        self.assertEqual(qs.count(), 0)

    def test_overdue_leases_includes_past_long_term(self):
        make_reservation(self.site, checkin_offset=-35, checkout_offset=-1, is_long_term=True)
        qs = Reservation.objects.get_queryset().overdue_leases_on(self.today)
        self.assertEqual(qs.count(), 1)

    def test_overdue_leases_excludes_short_term(self):
        make_reservation(self.site, checkin_offset=-5, checkout_offset=-1, is_long_term=False)
        qs = Reservation.objects.get_queryset().overdue_leases_on(self.today)
        self.assertEqual(qs.count(), 0)


# ---------------------------------------------------------------------------
# expiring_leases_on()
# ---------------------------------------------------------------------------

class ExpiringLeasesTest(TestCase):
    def setUp(self):
        self.site = make_site()
        self.today = timezone.now().date()

    def test_expiring_lease_on_today(self):
        make_reservation(self.site, checkin_offset=-30, checkout_offset=0, is_long_term=True)
        qs = Reservation.objects.get_queryset().expiring_leases_on(self.today)
        self.assertEqual(qs.count(), 1)

    def test_expiring_lease_excludes_short_term(self):
        make_reservation(self.site, checkin_offset=-3, checkout_offset=0, is_long_term=False)
        qs = Reservation.objects.get_queryset().expiring_leases_on(self.today)
        self.assertEqual(qs.count(), 0)

    def test_expiring_lease_excludes_future_checkout(self):
        make_reservation(self.site, checkin_offset=-30, checkout_offset=5, is_long_term=True)
        qs = Reservation.objects.get_queryset().expiring_leases_on(self.today)
        self.assertEqual(qs.count(), 0)


# ---------------------------------------------------------------------------
# upcoming()
# ---------------------------------------------------------------------------

class UpcomingTest(TestCase):
    def setUp(self):
        self.site = make_site()
        self.today = timezone.now().date()

    def test_upcoming_includes_future_checkin(self):
        make_reservation(self.site, checkin_offset=1, checkout_offset=4)
        qs = Reservation.objects.get_queryset().upcoming()
        self.assertEqual(qs.count(), 1)

    def test_upcoming_excludes_today_checkin(self):
        make_reservation(self.site, checkin_offset=0, checkout_offset=3)
        qs = Reservation.objects.get_queryset().upcoming()
        self.assertEqual(qs.count(), 0)

    def test_upcoming_excludes_past_checkin(self):
        make_reservation(self.site, checkin_offset=-2, checkout_offset=1)
        qs = Reservation.objects.get_queryset().upcoming()
        self.assertEqual(qs.count(), 0)


# ---------------------------------------------------------------------------
# current_and_upcoming()
# ---------------------------------------------------------------------------

class CurrentAndUpcomingTest(TestCase):
    def setUp(self):
        self.site = make_site()
        self.today = timezone.now().date()

    def test_includes_currently_occupied(self):
        # checked in yesterday, checks out tomorrow
        make_reservation(self.site, checkin_offset=-1, checkout_offset=1)
        qs = Reservation.objects.get_queryset().current_and_upcoming()
        self.assertEqual(qs.count(), 1)

    def test_includes_checking_out_today(self):
        make_reservation(self.site, checkin_offset=-3, checkout_offset=0)
        qs = Reservation.objects.get_queryset().current_and_upcoming()
        self.assertEqual(qs.count(), 1)

    def test_includes_future_reservation(self):
        make_reservation(self.site, checkin_offset=2, checkout_offset=5)
        qs = Reservation.objects.get_queryset().current_and_upcoming()
        self.assertEqual(qs.count(), 1)

    def test_excludes_past_reservation(self):
        make_reservation(self.site, checkin_offset=-5, checkout_offset=-1)
        qs = Reservation.objects.get_queryset().current_and_upcoming()
        self.assertEqual(qs.count(), 0)

    def test_chaining_with_active(self):
        # confirmed checkout in the future should NOT appear
        make_reservation(self.site, checkin_offset=1, checkout_offset=4, confirmed_checkout=True)
        # unconfirmed checkout in the future SHOULD appear
        make_reservation(self.site, checkin_offset=1, checkout_offset=4, confirmed_checkout=False)
        qs = Reservation.objects.active().current_and_upcoming()
        self.assertEqual(qs.count(), 1)


# ---------------------------------------------------------------------------
# overlapping() — most critical, protects against double booking
# ---------------------------------------------------------------------------

class OverlappingTest(TestCase):
    def setUp(self):
        self.site = make_site()
        self.now = timezone.now()
        # Base reservation: days 0-5
        self.base = make_reservation(
            self.site,
            checkin_offset=0,
            checkout_offset=5,
        )

    def _dt(self, offset):
        """Return a datetime offset days from now."""
        return self.now + timedelta(days=offset)

    def test_fully_overlapping(self):
        # new reservation completely inside existing
        qs = Reservation.objects.get_queryset().overlapping(
            self._dt(1), self._dt(4)
        )
        self.assertEqual(qs.count(), 1)

    def test_partially_overlapping_start(self):
        # new reservation starts before, ends inside
        qs = Reservation.objects.get_queryset().overlapping(
            self._dt(-2), self._dt(3)
        )
        self.assertEqual(qs.count(), 1)

    def test_partially_overlapping_end(self):
        # new reservation starts inside, ends after
        qs = Reservation.objects.get_queryset().overlapping(
            self._dt(3), self._dt(7)
        )
        self.assertEqual(qs.count(), 1)

    def test_surrounding_overlap(self):
        # new reservation completely surrounds existing
        qs = Reservation.objects.get_queryset().overlapping(
            self._dt(-1), self._dt(6)
        )
        self.assertEqual(qs.count(), 1)

    def test_adjacent_checkout_does_not_overlap(self):
        # Existing reservation: day 0 noon → day 5 at 2PM
        # New reservation: day 5 at 5PM → day 8 noon
        # Should NOT conflict since new checkin is after existing checkout
        base = self.now.replace(hour=12, minute=0, second=0, microsecond=0)
        
        # recreate base reservation with explicit clean times
        self.base.checkin = base
        self.base.checkout = base + timedelta(days=5, hours=2)  # day 5 @ 2PM
        self.base.save()

        new_checkin = base + timedelta(days=5, hours=5)   # day 5 @ 5PM
        new_checkout = base + timedelta(days=8)

        qs = Reservation.objects.get_queryset().overlapping(new_checkin, new_checkout)
        self.assertEqual(qs.count(), 0)

    def test_adjacent_checkin_does_not_overlap(self):
        # Existing reservation: day 0 noon → day 5 at 2PM
        # New reservation: day -3 → day 0 at 10AM (checks out before existing checks in)
        base = self.now.replace(hour=12, minute=0, second=0, microsecond=0)

        self.base.checkin = base
        self.base.checkout = base + timedelta(days=5, hours=2)
        self.base.save()

        new_checkin = base - timedelta(days=3)
        new_checkout = base - timedelta(hours=2)  # 10AM, before existing noon checkin

        qs = Reservation.objects.get_queryset().overlapping(new_checkin, new_checkout)
        self.assertEqual(qs.count(), 0)

    def test_same_day_turnover_does_not_overlap(self):
        """
        Guest A checks out at 2PM, Guest B checks in at 5PM same day.
        Should NOT be flagged as a conflict.
        """
        base = self.now.replace(hour=12, minute=0, second=0, microsecond=0)

        self.base.checkin = base - timedelta(days=3)
        self.base.checkout = base + timedelta(hours=2)  # 2PM today
        self.base.save()

        new_checkin = base + timedelta(hours=5)   # 5PM today
        new_checkout = base + timedelta(days=3)

        qs = Reservation.objects.get_queryset().overlapping(new_checkin, new_checkout)
        self.assertEqual(qs.count(), 0)

    def test_same_day_overlapping_times_conflict(self):
        """
        Guest A checks out at 5PM, Guest B checks in at 2PM same day.
        SHOULD be flagged as a conflict.
        """
        base = self.now.replace(hour=12, minute=0, second=0, microsecond=0)

        self.base.checkin = base - timedelta(days=3)
        self.base.checkout = base + timedelta(hours=5)  # 5PM today
        self.base.save()

        new_checkin = base + timedelta(hours=2)   # 2PM today — before existing checkout
        new_checkout = base + timedelta(days=3)

        qs = Reservation.objects.get_queryset().overlapping(new_checkin, new_checkout)
        self.assertEqual(qs.count(), 1)

    def test_completely_before_does_not_overlap(self):
        qs = Reservation.objects.get_queryset().overlapping(
            self._dt(-5), self._dt(-1)
        )
        self.assertEqual(qs.count(), 0)

    def test_completely_after_does_not_overlap(self):
        qs = Reservation.objects.get_queryset().overlapping(
            self._dt(6), self._dt(10)
        )
        self.assertEqual(qs.count(), 0)

    def test_multiple_overlapping_reservations(self):
        # add a second overlapping reservation on the same site
        make_reservation(self.site, checkin_offset=2, checkout_offset=7)
        qs = Reservation.objects.get_queryset().overlapping(
            self._dt(3), self._dt(6)
        )
        self.assertEqual(qs.count(), 2)

    def test_overlap_isolated_to_correct_site(self):
        # reservation on a different site should not be returned
        other_site = make_site(lot_id="B1")
        make_reservation(other_site, checkin_offset=1, checkout_offset=4)
        qs = Reservation.objects.filter(site=self.site).overlapping(
            self._dt(1), self._dt(4)
        )
        self.assertEqual(qs.count(), 1)


# ---------------------------------------------------------------------------
# occupied_on()
# ---------------------------------------------------------------------------

class OccupiedOnTest(TestCase):
    def setUp(self):
        self.site = make_site()
        self.today = timezone.now().date()

    def test_occupied_on_includes_current_reservation(self):
        make_reservation(self.site, checkin_offset=-1, checkout_offset=1)
        qs = Reservation.objects.occupied_on(self.today)
        self.assertEqual(qs.count(), 1)

    def test_occupied_on_includes_checkin_today(self):
        make_reservation(self.site, checkin_offset=0, checkout_offset=2)
        qs = Reservation.objects.occupied_on(self.today)
        self.assertEqual(qs.count(), 1)

    def test_occupied_on_includes_checkout_today(self):
        make_reservation(self.site, checkin_offset=-2, checkout_offset=0)
        qs = Reservation.objects.occupied_on(self.today)
        self.assertEqual(qs.count(), 1)

    def test_occupied_on_excludes_confirmed_checkout(self):
        make_reservation(self.site, checkin_offset=-1, checkout_offset=1, confirmed_checkout=True)
        qs = Reservation.objects.occupied_on(self.today)
        self.assertEqual(qs.count(), 0)

    def test_occupied_on_excludes_future_reservation(self):
        make_reservation(self.site, checkin_offset=1, checkout_offset=4)
        qs = Reservation.objects.occupied_on(self.today)
        self.assertEqual(qs.count(), 0)

    def test_occupied_on_excludes_past_reservation(self):
        make_reservation(self.site, checkin_offset=-4, checkout_offset=-1)
        qs = Reservation.objects.occupied_on(self.today)
        self.assertEqual(qs.count(), 0)


# ---------------------------------------------------------------------------
# __str__
# ---------------------------------------------------------------------------

class ReservationStrTest(TestCase):
    def test_str_returns_name(self):
        site = make_site()
        res = make_reservation(site, name="John Smith")
        self.assertEqual(str(res), "John Smith")