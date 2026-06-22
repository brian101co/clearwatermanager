from django.urls import path
from .views import (
    SiteDetailView,
    SiteListView,
    EditSiteView,
    CreateSiteView,
    RetireSiteView
)

urlpatterns = [
    path("", SiteListView.as_view(), name="site-list"),
    path("<int:id>/", SiteDetailView.as_view(), name="site-detail"),
    path("create/", CreateSiteView.as_view(), name="site-create"),
    path("edit/<int:id>/", EditSiteView.as_view(), name="site-edit"),
    path("retire/<int:id>/", RetireSiteView.as_view(), name="site-delete"),
]
