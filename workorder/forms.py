from django import forms
from django.db.models import fields
from .models import WorkOrder
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

class WorkorderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ('title', 'site', 'description',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].label = "Title"
        self.fields["site"].label = "Lot"
        self.fields["description"].label = "Description of the Issue"

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("title", placeholder="title"),
            Field("site", placeholder="lot"),
            Field("description", rows="5"),
            Submit("submit", "Submit", css_class="btn pure-material-button-contained")
        )
