from django.contrib import admin
from django.urls import path, include
from sites import views as site_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from .settings import DEBUG, MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('', include("manager.urls")),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('workorders/', include("workorder.urls")),
    path('sites/', include("sites.urls")),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('site/info/<str:site>', site_views.get_site_info, name="site_info"),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

if DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]