from django import forms

class NameForm(forms.Form):

    token = forms.CharField(max_length=100)
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)

