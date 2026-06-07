from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaymentListView.as_view(), name='payment-list'),
    path('<int:id>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    path('create/', views.CreatePaymentView.as_view(), name='payment-create'),
    path('<int:id>/edit/', views.UpdatePaymentView.as_view(), name='payment-edit'),
    path('<int:id>/delete/', views.DeletePaymentView.as_view(), name='payment-delete'),
]