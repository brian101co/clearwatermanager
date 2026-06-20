from django import forms
from .models import Site
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Row, Column

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = [
            'lot_id', 'info', 'lot_type', 'under_maintenance',
            'water', 'electric_30amp', 'electric_50amp', 'sewer',
            'wifi', 'max_length_ft', 'nightly_rate', 'weekly_rate',
            'monthly_rate', 'notes'
        ]
        labels = {
            "lot_id": "Lot Number",
            "info": "Information",
            "lot_type": "Lot Type",
            "under_maintenance": "Under Maintenance",
            "water": "Water Hookup",
            "electric_30amp": "30 AMP",
            "electric_50amp": "50 AMP",
            "sewer": "Sewer Hookup",
            "wifi": "WiFi",
            "max_length_ft": "Max Length (ft)",
            "nightly_rate": "Nightly Rate",
            "weekly_rate": "Weekly Rate",
            "monthly_rate": "Monthly Rate",
            "notes": "Notes",
        }
        help_texts = {
            "max_length_ft": "Maximum RV length this lot can accommodate",
            "nightly_rate": "Leave blank if rate varies",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False 
        self.helper.layout = Layout(
            # Basic Info
            HTML('<h5 class="text-muted mt-2 mb-2">Basic Information</h5>'),
            Field("lot_id", placeholder="e.g. 12, 10C"),
            Field("lot_type"),
            Field("info"),
            
            # Amenities
            HTML('<h5 class="text-muted mt-4 mb-2">Amenities</h5>'),
            Row(
                Column(Field("water"), css_class="form-group col-md-4 mb-0"),
                Column(Field("sewer"), css_class="form-group col-md-4 mb-0"),
                Column(Field("wifi"), css_class="form-group col-md-4 mb-0"),
                Column(Field("electric_30amp"), css_class="form-group col-md-4 mb-0"),
                Column(Field("electric_50amp"), css_class="form-group col-md-4 mb-0"),
            ),
            
            # Details
            HTML('<h5 class="text-muted mt-4 mb-2">Details</h5>'),
            Field("max_length_ft", placeholder="e.g. 40"),
            Field("under_maintenance"),
            Field("notes"),

            # Pricing
            HTML('<h5 class="text-muted mt-4 mb-2">Pricing</h5>'),
            Row(
                Column(Field("nightly_rate", placeholder="00.00"), css_class="form-group col-md-4 mb-0"),
                Column(Field("weekly_rate", placeholder="00.00"), css_class="form-group col-md-4 mb-0"),
                Column(Field("monthly_rate", placeholder="00.00"), css_class="form-group col-md-4 mb-0"),
            ),
        )

    def _clean_non_negative_rate(self, field_name):
        value = self.cleaned_data.get(field_name)
        if value is not None and value < 0:
            raise forms.ValidationError("Rate cannot be negative.")
        return value

    def clean_nightly_rate(self):
        return self._clean_non_negative_rate("nightly_rate")

    def clean_weekly_rate(self):
        return self._clean_non_negative_rate("weekly_rate")

    def clean_monthly_rate(self):
        return self._clean_non_negative_rate("monthly_rate")

    def clean_lot_id(self):
        return self.cleaned_data["lot_id"].strip().upper()
