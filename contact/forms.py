from django import forms
from .models import Contact


class ContactForm(forms.Form):
    first_name = forms.CharField(required=True,  max_length=60)
    last_name = forms.CharField(required=True, max_length=60)
    email = forms.EmailField(required=True)
    message = forms.CharField(required=True, widget=forms.Textarea)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        #fields = ['first_name', 'last_name', 'email', 'message']
        fields = '__all__'