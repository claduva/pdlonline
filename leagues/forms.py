from django import forms
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from .models import application, coach, draft, left_pick, match,free_agency,trade_request
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

class MatchForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    week = forms.ChoiceField()
    playoff_week = forms.ChoiceField()

    class Meta:
        model = match
        fields = ['week','playoff_week','team1','team2']
        labels = {
            'team1':'Team 1',
            'team2':'Team 2',
        }
    
    def __init__(self, *args, **kwargs):
        coaches = kwargs.pop('coaches', None)
        szn = kwargs.pop('szn', None)
        super(MatchForm, self).__init__(*args, **kwargs)
        if coaches: 
            self.fields['team1'].queryset=coaches
            self.fields['team2'].queryset=coaches
        if szn:
            self.fields['week'].choices = [(None,"---------")]+[(week+1,week+1) for week in range(szn.seasonlength)]
            baseplayoffsoptions=['Quarterfinals','Semifinals','Finals']
            extraplayoffs=[]
            if szn.playoffslength>3:
                for i in range(szn.playoffslength-3):
                    extraplayoffs.append(f'Playoffs Week {i+1}')
            playoffsoptions=extraplayoffs+baseplayoffsoptions
            self.fields['playoff_week'].choices = [(None,"---------")]+[(week,week) for week in playoffsoptions]
        self.fields['week'].label="Week (Only select if regular season match)"
        self.fields['week'].required=False
        self.fields['playoff_week'].label="Playoff Week (Only select if playoff match)"
        self.fields['playoff_week'].required=False

class FreeAgencyForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))

    class Meta:
        model = free_agency
        fields = ['dropped_pokemon','added_pokemon']
    
    def __init__(self, *args, **kwargs):
        user_pokemon = kwargs.pop('user_pokemon', None)
        availablepokemon = kwargs.pop('availablepokemon', None)
        super(FreeAgencyForm, self).__init__(*args, **kwargs)
        if user_pokemon: self.fields['dropped_pokemon'].queryset=user_pokemon
        if availablepokemon: self.fields['added_pokemon'].queryset=availablepokemon
        self.fields['dropped_pokemon'].label="Pokemon to Drop"
        self.fields['added_pokemon'].label="Pokemon to Add"

class TradeRequestForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))

    class Meta:
        model = trade_request
        fields = ['offeredpokemon','requestedpokemon']
    
    def __init__(self, *args, **kwargs):
        user_pokemon = kwargs.pop('user_pokemon', None)
        availablepokemon = kwargs.pop('availablepokemon', None)
        super(TradeRequestForm, self).__init__(*args, **kwargs)
        if user_pokemon: self.fields['offeredpokemon'].queryset=user_pokemon
        if availablepokemon: self.fields['requestedpokemon'].queryset=availablepokemon
        self.fields['offeredpokemon'].label="Offered Pokemon"
        self.fields['requestedpokemon'].label="Requested Pokemon"
        self.fields['offeredpokemon'].label_from_instance = lambda obj: f'{obj.pokemon.name}'
        self.fields['requestedpokemon'].label_from_instance = lambda obj: f'{obj.team.teamname}: {obj.pokemon.name}'