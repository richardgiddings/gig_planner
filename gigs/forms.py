from django import forms
from .models import Gig
from bootstrap3_datetime.widgets import DateTimePicker

class GigForm(forms.ModelForm):
    """
    A form for a Task
    """
    class Meta:
        model = Gig
        fields = '__all__'

        widgets={
        'gig_date': DateTimePicker(
            options={"format": "YYYY-MM-DD", "pickTime": False},
            attrs={'placeholder': 'Use the button to the right to enter a date.'}),
        'gig_time': DateTimePicker(
            options={"format":"HH:mm", "pickDate":False},
            attrs={'placeholder': 'Use the button to the right to enter a time.'})
        }

    def __init__(self, *args, **kwargs):
        super(GigForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'