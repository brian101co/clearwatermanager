from django import forms
from .models import Payment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['customer', 'amount_due', 'amount_paid', 'status', 'method', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].label = 'Guest'
        self.fields['amount_due'].label = 'Amount Due'
        self.fields['amount_paid'].label = 'Amount Paid'
        self.fields['status'].label = 'Payment Status'
        self.fields['method'].label = 'Payment Method'
        self.fields['notes'].label = 'Notes'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('customer'),
            Field('amount_due', placeholder='0.00'),
            Field('amount_paid', placeholder='0.00'),
            Field('status'),
            Field('method'),
            Field('notes', rows='3'),
        )