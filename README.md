# Clearwater RV Management App

Clearwater RV Management Dashboard is an internal management tool built for park managers to manage reservations, track park maintenance through a work order system, and monitor park performance metrics.

## Reservation Management
The reservation management system allows managers to add, view, edit, and delete reservations. Reservations are categorized as either **short-term** or **long-term** based on a manager-defined flag, keeping the dashboard organized and easy to scan.

The availability checker allows managers to search by check-in and check-out datetime to find open sites, preventing double bookings. The system uses a universal overlap detection algorithm to catch all possible booking conflicts.

## Dashboard Notifications
The dashboard surfaces three real-time notification sections to help managers stay on top of daily activity:
- **Checking Out Tomorrow** — guests scheduled to check out tomorrow
- **Checking In Tomorrow** — guests arriving tomorrow
- **Expiring Leases** — long-term residents whose lease expires within 30 days

Each notification card includes a direct call button and a link to the full reservation detail page for quick access.

## Occupancy Rate
A live occupancy progress bar shows the percentage of lots currently occupied, giving managers an instant read on park capacity at a glance.

## Interactive Park Map
The interactive SVG park map shows managers which sites are currently available (green) or occupied (red) at a glance. Hovering over an occupied lot displays a tooltip showing the guest name and checkout date. Selecting a site on the map opens a modal displaying site information. A color legend is displayed below the map for quick reference.

## Site Management
The site management system allows managers to view, create, edit and delete park sites. Each site tracks amenities including water hookups, 30/50 amp electric, sewer, and WiFi availability, as well as lot type, maximum RV length, nightly rate, and maintenance status. Open work orders are displayed directly on each site detail page for a complete picture of site status.

## Work Order System
The work order system allows park managers to create, track, and manage site maintenance from a centralized dashboard. Work orders are categorized by type (electrical, plumbing, landscaping, cleaning, structural, appliance, general) and prioritized as Low, Normal, or High urgency. Work orders support estimated vs actual cost tracking, photo attachments, and recurring maintenance scheduling. The metrics page tracks associated maintenance costs over time, giving managers visibility into park operating costs.

## Tech Stack
- **Backend** — Python, Django
- **Frontend** — Bootstrap 4, JavaScript
- **Database** — SQLite (dev), MySQL (production)