import re

from django import forms
from .models import Reservation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit
from django.utils import timezone

class ReservationForm(forms.ModelForm):
    DATETIME_FORMAT = "%Y-%m-%dT%H:%M"

    class Meta:
        model = Reservation
        fields = ["name", "site", "checkin", "checkout", "phone_num", "is_long_term", "info"]
        labels = {
            "name": "Name",
            "site": "Lot No.",
            "checkin": "Checkin",
            "checkout": "Checkout",
            "phone_num": "Phone Number",
            "info": "Additional Information (optional)",
            "is_long_term": "Long Term Resident (optional)"
        }
        widgets = {
            "checkin": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "checkout": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "phone_num": forms.TextInput(attrs={"type": "tel"}),
            "info": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ("checkin", "checkout"):
            self.fields[f].input_formats = [self.DATETIME_FORMAT]

        if not self.instance.pk:
            self.fields["checkin"].initial = timezone.now()

        self.fields["name"].widget.attrs["autofocus"] = True
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("name", placeholder="Guest name"),
            Field("checkin"),
            Field("checkout"),
            Field("site", placeholder="Lot No."),
            Field("phone_num", placeholder="Phone Number"),
            Field("is_long_term"),
            Field("info"),
        )

    def clean(self):
        cleaned_data = super().clean()
        checkin, checkout = cleaned_data.get("checkin"), cleaned_data.get("checkout")

        if checkin and checkout and checkout <= checkin:
            self.add_error("checkout", "Checkout must be after checkin.")

        return cleaned_data
    
    def clean_site(self):
        return self.cleaned_data["site"].strip().upper()
    
    def clean_phone_num(self):
        digits = re.sub(r"\D", "", self.cleaned_data["phone_num"])
        if len(digits) != 10:
            raise forms.ValidationError("Enter a 10-digit phone number.")
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
