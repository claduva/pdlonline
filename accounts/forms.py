from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from timezone_field import TimeZoneFormField
from django.contrib.postgres.forms import SimpleArrayField, SplitArrayField

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class UserSettingsForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    timezone=TimeZoneFormField()
    #showdown_alts=SplitArrayField(forms.CharField(max_length=30,required=False), size=10, remove_trailing_nulls=True)
    showdown_alts = SimpleArrayField(forms.CharField(max_length=30))
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email','biography','timezone','showdown_alts']

    def __init__(self, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)
        self.fields['showdown_alts'].label="Pokemon Showdown Usernames/Alts"
        self.fields['showdown_alts'].help_text="Enter each username separated by commas. E.g.: pokemontrainer1,pokemontrainer2"