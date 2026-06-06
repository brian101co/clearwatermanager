from django import forms
from .models import Site
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = [
            'identifier', 'info', 'lot_type', 'under_maintenance',
            'water', 'electric_30amp', 'electric_50amp', 'sewer',
            'wifi', 'max_length_ft', 'nightly_rate', 'weekly_rate',
            'monthly_rate', 'notes'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["identifier"].label = "Lot Number"
        self.fields["info"].label = "Information"
        self.fields["lot_type"].label = "Lot Type"
        self.fields["under_maintenance"].label = "Under Maintenance"
        self.fields["water"].label = "Water Hookup"
        self.fields["electric_30amp"].label = "30 AMP"
        self.fields["electric_50amp"].label = "50 AMP"
        self.fields["sewer"].label = "Sewer Hookup"
        self.fields["wifi"].label = "WiFi"
        self.fields["max_length_ft"].label = "Max Length (ft)"
        self.fields["max_length_ft"].help_text = "Maximum RV length this lot can accommodate"
        self.fields["nightly_rate"].label = "Nightly Rate"
        self.fields["nightly_rate"].help_text = "Leave blank if rate varies"
        self.fields["weekly_rate"].label = "Weekly Rate"
        self.fields["weekly_rate"].help_text = "Weekly rate"
        self.fields["monthly_rate"].label = "Monthly Rate"
        self.fields["monthly_rate"].help_text = "Monthly rate"
        self.fields["notes"].label = "Notes"
        
        self.helper = FormHelper()
        self.helper.form_tag = False 
        self.helper.layout = Layout(
            # Basic Info
            HTML('<h6 class="text-muted mt-3 mb-2">Basic Information</h6>'),
            Field("identifier", placeholder="e.g. 12, 10C"),
            Field("lot_type"),
            Field("info"),
            
            # Amenities
            HTML('<h6 class="text-muted mt-3 mb-2">Amenities</h6>'),
            Field("water"),
            Field("sewer"),
            Field("wifi"),
            Field("electric_30amp"),
            Field("electric_50amp"),
            
            # Details
            HTML('<h6 class="text-muted mt-3 mb-2">Details</h6>'),
            Field("max_length_ft", placeholder="e.g. 40"),
            Field("under_maintenance"),
            Field("notes"),

            # Pricing
            HTML('<h6 class="text-muted mt-3 mb-2">Pricing</h6>'),
            Field("nightly_rate", placeholder="00.00"),
            Field("weekly_rate", placeholder="00.00"),
            Field("monthly_rate", placeholder="00.00"),
        )
