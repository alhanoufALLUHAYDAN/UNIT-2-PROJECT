from django import forms
from twist.models import TimeTwist

class TimeTwistForm(forms.ModelForm):
    class Meta:
        model = TimeTwist
        fields = ['title', 'content', 'entry_type', 'image']
