from django import forms
from .models import Customer
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Submit

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        widgets = {
            'start': forms.DateInput(attrs={'type': 'datetime-local'}),
            'end': forms.DateInput(attrs={'type': 'datetime-local'}),
            'phoneNum': forms.TextInput(attrs={'type': 'tel'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Name"
        self.fields["site"].label = "Lot"
        self.fields["start"].label = "Checkin"
        self.fields["end"].label = "Checkout"
        self.fields["phoneNum"].label = "Phone Number"
        self.fields["info"].label = "Additional Information"
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("name", placeholder="Enter name"),
            Field("site", placeholder="lot"),
            Field("start", placeholder="Checkin Date"),
            Field("end", placeholder="Checkout Date"),
            Field("phoneNum", placeholder="Phone Number"),
            Field("info", rows="3"),
            HTML('<button type="button" class="btn pure-material-button-contained bg-secondary mr-2" data-dismiss="modal">Close</button>'),
            Submit("submit", "Submit", css_class="btn pure-material-button-contained")
        )
