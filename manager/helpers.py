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
        return False
    return False


def get_reservation_type(checkin, checkout):
    """ Returns whether the reservations is daily (1), weekly (2), or monthly (3) """
    checkin_dt = pendulum.parse(checkin, tz="UTC")
    checkout_dt = pendulum.parse(checkout, tz="UTC")
    weeks = checkin_dt.diff(checkout_dt).in_weeks()
    months = checkin_dt.diff(checkout_dt).in_months()
    if months >= 1:
        return 3
    elif weeks >= 1:
        return 2
    return 1

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
