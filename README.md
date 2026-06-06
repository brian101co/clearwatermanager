# Clearwater RV Management App

Clearwater RV Management Dashboard is an internal management tool built for park managers to manage reservations, track park maintenance through a work order system, and monitor park performance metrics.

## Reservation Management
The reservation management system allows managers to add, view, edit, and delete reservations. Reservations are categorized as either **short-term** or **long-term** based on a manager-defined flag, keeping the dashboard organized and easy to scan.

The availability checker allows managers to search by check-in and check-out datetime to find open sites, preventing double bookings. The system uses a universal overlap detection algorithm to catch all possible booking conflicts.

## Dashboard Notifications
The dashboard surfaces three real-time notification sections to help managers stay on top of daily activity:
- **Checking Out Soon** — guests scheduled to check out tomorrow
- **Checking In Soon** — guests arriving tomorrow
- **Expiring Leases** — long-term residents whose lease expires within 30 days

Each notification card includes a direct call button and a link to the full reservation detail page for quick access.

## Occupancy Rate
A live occupancy progress bar shows the percentage of lots currently occupied, giving managers an instant read on park capacity at a glance.

## Interactive Park Map
The interactive SVG park map shows managers which sites are currently available (green) or occupied (red) at a glance. Selecting a site on the map opens a modal displaying site information including unit size capacity and any relevant notes.

## Work Order System
The work order system allows park managers to create, track, and manage site maintenance from a centralized dashboard. Work orders are prioritized as Low, Normal, or High urgency. Maintenance crews can view open work orders and mark them as complete when finished. The metrics page tracks associated maintenance costs over time, giving managers visibility into park operating costs.

## Tech Stack
- **Backend** — Python, Django
- **Frontend** — Bootstrap 4, JavaScript
- **Database** — SQLite (dev), MySQL (production)