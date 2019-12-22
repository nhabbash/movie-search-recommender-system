from django import forms

class SearchForm(forms.Form):
    # See https://docs.djangoproject.com/en/3.0/ref/forms/fields/ and https://docs.djangoproject.com/en/3.0/topics/forms/
    query = forms.CharField(required=False, label='Search...')
    profile = forms.CharField(required=False, label='User...')
    fuzzy = forms.BooleanField(required=False)
    personalized = forms.BooleanField(required=False)
    synonyms = forms.BooleanField(required=False)