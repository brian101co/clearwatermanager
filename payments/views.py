from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Payment
from .forms import PaymentForm

class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    context_object_name = 'payments'
    template_name = 'payments/list_payments.html'
    ordering = ['-created_at']

    def get_queryset(self):
        status = self.request.GET.get('status')
        if status:
            return Payment.objects.filter(status=status).order_by('-created_at')
        return Payment.objects.all().order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["unpaid_count"] = Payment.objects.filter(status='unpaid').count()
        context["partial_count"] = Payment.objects.filter(status='partial').count()
        context["paid_count"] = Payment.objects.filter(status='paid').count()
        return context


class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = Payment
    pk_url_kwarg = 'id'
    context_object_name = 'payment'
    template_name = 'payments/payment_detail.html'


class CreatePaymentView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    success_url = reverse_lazy('payment-list')
    template_name = 'payments/create_payment.html'


class UpdatePaymentView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('payment-list')
    template_name = 'payments/edit_payment.html'


class DeletePaymentView(LoginRequiredMixin, DeleteView):
    model = Payment
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('payment-list')
    template_name = 'payments/delete_payment.html'