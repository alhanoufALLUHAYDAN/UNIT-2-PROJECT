from django import forms
from main.models import Message


class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'content']  