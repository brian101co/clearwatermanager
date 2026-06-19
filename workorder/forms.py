from django import forms
from django.db.models import fields
from .models import WorkOrder
from sites.models import Site
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML

class WorkorderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = (
            'title',
            'site',
            'category',
            'priority',
            'description',
            'estimated_cost',
            'cost',
            'image',
            'is_recurring',
            'recurring_interval',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].label = "Title"
        self.fields["site"].label = "Lot"
        self.fields["site"].queryset = Site.objects.order_by("lot_id")
        self.fields["category"].label = "Category"
        self.fields["description"].label = "Description of the Issue"
        self.fields["priority"].label = "Urgency Level"
        self.fields["estimated_cost"].label = "Estimated Cost"
        self.fields["cost"].label = "Actual Cost"
        self.fields["image"].label = "Attach Photo"
        self.fields["image"].required = False
        self.fields["is_recurring"].label = "Recurring Work Order"
        self.fields["recurring_interval"].label = "Repeat Every (days)"
        self.fields["recurring_interval"].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            # Basic Info
            Field("title", placeholder="Title"),
            Field("site"),
            Field("category"),
            Field("priority"),
            Field("assigned_to"),
            Field("description", rows="5"),

            # Cost
            HTML("""
                <div class="form-group">
                    <label for="estimated_cost">Estimated Cost</label>
                    <div class="input-group">
                        <div class="input-group-prepend">
                            <div class="input-group-text">$</div>
                        </div>
                        <input type="number" class="form-control" id="estimated_cost" 
                               name="estimated_cost" placeholder="00.00" step="0.01">
                    </div>
                </div>
                <div class="form-group">
                    <label for="actual_cost">Actual Cost</label>
                    <div class="input-group">
                        <div class="input-group-prepend">
                            <div class="input-group-text">$</div>
                        </div>
                        <input type="number" class="form-control" id="cost" 
                               name="cost" placeholder="00.00" step="0.01">
                    </div>
                </div>
            """),

            # Photo
            Field("image"),

            # Recurring
            Field("is_recurring"),
            HTML("""
                <div id="recurring-interval-container" style="display:none;">
            """),
            Field("recurring_interval", placeholder="e.g. 7 for weekly, 30 for monthly"),
            HTML("</div>"),

            Submit("submit", "Submit", css_class="btn pure-material-button-contained")
        )
