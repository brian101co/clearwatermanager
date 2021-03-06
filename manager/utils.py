from datetime import timedelta

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
