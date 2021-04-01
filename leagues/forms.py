from django import forms
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from .models import application, coach
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

class ApplicationForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Apply', css_class='btn-primary'))
    
    class Meta:
        model = application
        fields = ['teamname','teamabbreviation','subleagues','alternate','showdown_username','resume','replays',]
        labels = {
            'teamname':'What is you team name? This can be changed later.',
            'teamabbreviation':'What is you team abbreviation? This can be changed later.',
            'subleagues':'What subleagues are you applying for? Select all that apply.',
            'alternate':'Would you be willing to serve as an alternate if not selected? Check if yes.',
            'showdown_username':'What is the main Showdown username you use, if any?',
            'resume':'What is your draft league resume? Include number of seasons played, league names, and how well you have done.',
            'replays':'Include links to any replays you would like to be considered here.',
        }
        help_texts={
            'subleagues':'Hold "Ctrl" or "Command" and click.',
        }
    

