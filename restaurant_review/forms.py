"""
Definition of forms.
"""

from django import forms
from django.utils.translation import gettext_lazy as _


class UserForm(forms.Form):
    twitter = forms.CharField()
    email = forms.EmailField()
    ordinals_address = forms.CharField()

class AccessForm(forms.Form):
    access_code = forms.CharField()