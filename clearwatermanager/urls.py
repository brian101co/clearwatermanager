from django.contrib import admin
from django.urls import path, include
from manager import views

urlpatterns = [
    path('', views.loginuser, name="loginuser"),
    path('dashboard/', views.index, name='home'),
    path('calendar/', views.calendar, name="calendar"),
    path('dashboard/delete/<int:id>', views.delete, name="delete"),
    path('dashboard/edit/<int:id>', views.edit, name="edit"),
    path('addcustomer/', views.addCustomer, name="addcustomer"),
    path('avaliable/', views.getAvaliability, name="avaliable"),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]
