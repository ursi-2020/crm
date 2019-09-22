from django import forms
class CustomerForm(forms.Form):
    file = forms.FileField() # for creating file input