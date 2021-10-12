from django.contrib import admin
from django.urls import path, include
from manager import views as manager_views
from sites import views as site_views

urlpatterns = [
    path('', manager_views.loginuser, name="loginuser"),
    path('dashboard/', manager_views.index, name='home'),
    path('dashboard/delete/<int:id>', manager_views.delete, name="delete"),
    path('dashboard/edit/<int:id>', manager_views.edit, name="edit"),
    path('dashboard/reservation/<int:id>', manager_views.reservation_detail, name="reservation-detail"),
    path('addcustomer/', manager_views.addCustomer, name="addcustomer"),
    path('avaliable/', manager_views.getAvaliability, name="avaliable"),
    path('site/info/<str:site>', site_views.get_site_info, name="site_info"),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]
