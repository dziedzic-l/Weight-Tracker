from django import forms

from .models import Measure, Profile, User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['height']


class MeasureForm(forms.ModelForm):
    class Meta:
        model = Measure
        fields = ['weight', 'date']
        exclude = ('user', )
