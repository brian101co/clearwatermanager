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
        fields = ["name", "site", "start", "end", "phoneNum", "is_long_term", "info"]
        labels = {
            "name": "Name",
            "site": "Lot No.",
            "start": "Checkin",
            "end": "Checkout",
            "phoneNum": "Phone Number",
            "info": "Additional Information (optional)",
            "is_long_term": "Long Term Resident (optional)"
        }
        widgets = {
            "start": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "end": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "phoneNum": forms.TextInput(attrs={"type": "tel"}),
            "info": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in ("start", "end"):
            self.fields[f].input_formats = [self.DATETIME_FORMAT]

        if not self.instance.pk:
            self.fields["start"].initial = timezone.now()

        self.fields["name"].widget.attrs["autofocus"] = True
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("name", placeholder="Guest name"),
            Field("start"),
            Field("end"),
            Field("site", placeholder="Lot No."),
            Field("phoneNum", placeholder="Phone Number"),
            Field("is_long_term"),
            Field("info"),
            HTML('<button type="button" class="btn pure-material-button-contained bg-secondary mr-2" data-dismiss="modal">Close</button>'),
            Submit("submit", "Submit", css_class="btn pure-material-button-contained"),
        )

    def clean(self):
        cleaned_data = super().clean()
        start, end = cleaned_data.get("start"), cleaned_data.get("end")

        if start and end and end <= start:
            self.add_error("end", "Checkout must be after checkin.")

        return cleaned_data
    
    def clean_site(self):
        return self.cleaned_data["site"].strip().upper()
    
    def clean_phoneNum(self):
        digits = re.sub(r"\D", "", self.cleaned_data["phoneNum"])
        if len(digits) != 10:
            raise forms.ValidationError("Enter a 10-digit phone number.")
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
