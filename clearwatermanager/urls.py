from django.contrib import admin
from datetime import datetime
from django.urls import path, include, register_converter
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from .settings import DEBUG, MEDIA_URL, MEDIA_ROOT
from reservations.api_views import (
    api_get_reservation_by_lot,
    api_get_reservations_on,
)
from workorder.views import (
    api_workorders_by_lot
)
from sites.views import (
    api_site_by_lot_id,
    api_sites_under_maintenance,
)

class DateConverter:
    regex = r'\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d').date()

    def to_url(self, value):
        return value.strftime('%Y-%m-%d')

register_converter(DateConverter, 'date')

# Page URLs
urlpatterns = [
    path('', include("dashboard.urls")),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('workorders/', include("workorder.urls")),
    path('sites/', include("sites.urls")),
    path('payments/', include("payments.urls")),
    path('metrics/', include("metrics.urls")),
    path('reservations/', include("reservations.urls")),
    path('admin/', admin.site.urls),
]

# API Endpoints
urlpatterns += [
    path('api/reservations/on/<date:date>/', api_get_reservations_on, name="api-reservations-on"),
    path('api/reservations/by-lot/<str:lot_id>/', api_get_reservation_by_lot, name="api-reservations-by-lot"),
    path('api/sites/under-maintenance/', api_sites_under_maintenance, name="api-sites-under-maintenance"),
    path('api/sites/<str:lot_id>/', api_site_by_lot_id, name="api-sites-by-lot"),
    path('api/workorders/by-lot/<str:lot_id>/', api_workorders_by_lot, name="api-workorders-by-lot"),
]


handler400 = 'reservations.views.handler400'
handler403 = 'reservations.views.handler403'
handler404 = 'reservations.views.handler404'
handler500 = 'reservations.views.handler500'

if DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)