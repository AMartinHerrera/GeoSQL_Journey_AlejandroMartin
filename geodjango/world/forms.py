
# In this file you add the forms that you application need to use

from django import forms
from .models import Stops

class QueryInputForm(forms.Form):

    query = forms.CharField()
