from django import forms
from .models import Stops

class QueryInputForm(forms.Form):

    query = forms.CharField()
