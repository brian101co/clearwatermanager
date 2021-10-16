import pendulum
from datetime import timedelta

def is_double_booked(reservations, checkin, checkout):
    """ Returns True if double booked and False if not. """
    checkin_dt = pendulum.parse(checkin, tz="UTC")
    checkout_dt = pendulum.parse(checkout, tz="UTC")
    if reservations:
        for reservation in reservations:
            if checkin_dt >= reservation.start and checkin_dt <= reservation.end:
                return True
            elif checkin_dt <= reservation.start and checkout_dt > reservation.start:
                return True
            else:
                return False
    return False


def get_reservation_type(checkin, checkout):
    """ Returns whether the reservations is daily (0), weekly (1), or monthly (2) """
    checkin_dt = pendulum.parse(checkin, tz="UTC")
    checkout_dt = pendulum.parse(checkout, tz="UTC")
    days = checkin_dt.diff(checkout_dt).in_days()
    if days < 7:
        return 0
    elif days >= 7 and days <= 28:
        return 1
    return 2

def get_long_term_reservations(customer_list):
    filtered_customers = []
    for customer in customer_list:
        delta = customer.end - customer.start
        longterm = timedelta(days=180)

        if delta > longterm:
            filtered_customers.append(customer)

    return filtered_customers

def get_short_term_reservations(customer_list):
    filtered_customers = []
    for customer in customer_list:
        delta = customer.end - customer.start
        longterm = timedelta(days=180)

        if delta < longterm:
            filtered_customers.append(customer)

    return filtered_customers
