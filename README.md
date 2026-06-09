# Clearwater RV Management App

Clearwater RV Management Dashboard is an internal management tool built for park managers to manage reservations, track park maintenance through a work order system, and monitor park performance metrics.

## Reservation Management
The reservation management system allows managers to add, view, edit, and delete reservations. Reservations are categorized as either **short-term** or **long-term** based on a manager-defined flag, keeping the dashboard organized and easy to scan.

The availability checker allows managers to search by check-in and check-out datetime to find open sites, preventing double bookings. Available sites display full amenity details including hookup types, lot size and nightly rate. Selecting an available site pre-fills the reservation form with the site number and dates.

The reservation detail page displays full reservation information including duration of stay, days remaining, site amenities, estimated cost breakdown with weekly and monthly discount rates, sales tax calculation and payment status.

## Checkout Workflow
Reservations follow a controlled checkout process to prevent double bookings and ensure accurate occupancy tracking. Rather than auto-checking guests out, the manager manually confirms each checkout after physically verifying the lot is clear. This ensures lots are never freed up prematurely and cancellation metrics remain accurate.

## Dashboard Notifications
The dashboard surfaces five real-time notification sections to help managers stay on top of daily activity:
- **Overdue Checkouts** — guests whose checkout date has already passed, requiring immediate follow up
- **Checking Out Today** — guests scheduled to check out today
- **Checking Out Tomorrow** — guests scheduled to check out tomorrow
- **Checking In Tomorrow** — guests arriving tomorrow
- **Expiring Leases** — long-term residents whose lease expires today

Each notification card includes a direct call button, a link to the reservation detail page, and a confirm checkout button where applicable.

## Occupancy Rate
A live occupancy progress bar shows the percentage of lots currently occupied, giving managers an instant read on park capacity at a glance.

## Interactive Park Map
The interactive SVG park map shows managers which sites are currently available (green) or occupied (red) at a glance. Hovering over an occupied lot displays a tooltip showing the guest name and checkout date. Selecting a site on the map opens a modal displaying site information. A color legend is displayed below the map for quick reference.

## Site Management
The site management system allows managers to view, create, edit and delete park sites. Each site tracks amenities including water hookups, 30/50 amp electric, sewer, and WiFi availability, as well as lot type, maximum RV length, nightly, weekly and monthly rates, and maintenance status. Open work orders are displayed directly on each site detail page for a complete picture of site status.

## Work Order System
The work order system allows park managers to create, track, and manage site maintenance from a centralized dashboard. Work orders are categorized by type (electrical, plumbing, landscaping, cleaning, structural, appliance, general) and prioritized as Low, Normal, or High urgency. Work orders support estimated vs actual cost tracking, photo attachments, and recurring maintenance scheduling. The metrics page tracks associated maintenance costs over time, giving managers visibility into park operating costs.

## Payments
The payments system allows managers to track guest payments against reservations. Payments are tracked by status — unpaid, partial, or paid. The payments list provides a summary of outstanding balances with filter tabs for quick access to unpaid and partial payments. Payment status is visible directly on the reservation detail page.

## Metrics & Reporting
The metrics page provides visual reporting on park performance using interactive Plotly charts. Year over year comparisons are available for reservations and maintenance costs. Summary stat cards display total reservations, cancellations, cancellation rate and maintenance costs with trend indicators showing percentage change vs the previous year. Available charts include:
- **Reservations per Month** — year over year comparison
- **Cancellations per Month** — monthly breakdown
- **Maintenance Costs** — year over year comparison
- **Most Popular Sites** — all time booking frequency
- **Long Term vs Short Term** — reservation type breakdown

## App Structure
The application is organized into focused Django apps following the single responsibility principle:
- **dashboard** — daily operations, map, notifications, occupancy
- **reservations** — reservation management and availability checker
- **sites** — site and amenity management
- **workorder** — maintenance work order system
- **payments** — payment tracking
- **metrics** — reporting and analytics

## Tech Stack
- **Backend** — Python 3.9, Django 3.2.25
- **Frontend** — Bootstrap 4, JavaScript, Plotly
- **Database** — SQLite (dev), MySQL (production)
