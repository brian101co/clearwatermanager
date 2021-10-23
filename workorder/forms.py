from django import forms
from django.db.models import fields
from .models import WorkOrder
from sites.models import Site
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML

class WorkorderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ('title', 'site', 'priority', 'description', 'cost', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].label = "Title"
        self.fields["site"].label = "Lot"
        self.fields["site"].queryset = Site.objects.order_by("identifier")
        self.fields["description"].label = "Description of the Issue"
        self.fields["priority"].label = "Urgency Level"

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("title", placeholder="title"),
            Field("site", placeholder="lot"),
            Field("priority"),
            Field("description", rows="5"),
            HTML("""
                <div class="form-group">
                    <label for="cost">Maintenance Cost</label>
                    <div class="input-group">
                        <div class="input-group-prepend">
                        <div class="input-group-text">$</div>
                        </div>
                        <input type="number" class="form-control" id="cost" name="cost" placeholder="00.00">
                    </div>
                </div>
            """),
            Submit("submit", "Submit", css_class="btn pure-material-button-contained")
        )
