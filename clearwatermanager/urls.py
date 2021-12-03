from django.contrib import admin
from django.urls import path, include
from sites import views as site_views
from .settings import DEBUG

urlpatterns = [
    path('', include("manager.urls")),
    path('workorders/', include("workorder.urls")),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('site/info/<str:site>', site_views.get_site_info, name="site_info"),
]

if DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]