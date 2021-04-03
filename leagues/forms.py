from django import forms
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from .models import application, coach, draft, left_pick
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
    
    def __init__(self, *args, **kwargs):
        loi = kwargs.pop('loi', None)
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['subleagues'].queryset=loi.subleagues.all()

class DraftForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_show_labels = False

    class Meta:
        model = draft
        fields = ['pokemon']
    
    def __init__(self, *args, **kwargs):
        availablepokemon = kwargs.pop('availablepokemon', None)
        super(DraftForm, self).__init__(*args, **kwargs)
        if availablepokemon: self.fields['pokemon'].queryset=availablepokemon

class LeftPickForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Add', css_class='btn-primary'))
    helper.form_show_labels = False

    class Meta:
        model = left_pick
        fields = ['pokemon']
    
    def __init__(self, *args, **kwargs):
        availablepokemon = kwargs.pop('availablepokemon', None)
        super(LeftPickForm, self).__init__(*args, **kwargs)
        if availablepokemon: self.fields['pokemon'].queryset=availablepokemon