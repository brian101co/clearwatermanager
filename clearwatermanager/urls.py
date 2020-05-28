from django.contrib import admin
from django.urls import path, include
from manager import views

urlpatterns = [
    path('', views.loginuser, name="loginuser"),
    path('dashboard/', views.index, name='home'),
    path('calendar/', views.calendar, name="calendar"),
    path('events/', views.event, name="events"),
    path('dashboard/delete/<int:id>', views.delete, name="delete"),
    path('addcustomer/', views.addCustomer, name="addcustomer"),
    path('admin/', admin.site.urls),
]
