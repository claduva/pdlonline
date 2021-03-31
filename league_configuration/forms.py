from django import forms
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from .models import league, league_configuration, subleague, league_tier, rules, season, conference, division
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

class CreateLeagueForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Next', css_class='btn-primary'))

    class Meta:
        model = league
        fields = ['name','abbreviation','logo','platform']
        labels = {
            'name': 'League Name',
            'abbreviation': 'League Abbreviation',
        }
        help_texts = {
            'name': 'e.g. All Star Premier League',
            'abbreviation': 'e.g. ASPL',
            'logo': 'Try uploading image to Discord, right-clicking, and selecting "Copy Image Address"',
        }

class LeagueConfigurationForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))

    class Meta:
        model = league_configuration
        fields = ['number_of_subleagues','allows_cross_subleague_matches','teambased']
        labels = {
            'number_of_subleagues': 'How many subleagues will your league have?',
            'allows_cross_subleague_matches': 'Will your league allow matches accross subleagues?',
            'teambased': "Is your league team-based?"
        }
        help_texts = {
            'number_of_subleagues': 'Generally, you will put 1 for this. This is the number of independent drafts there will be. For example, if you will have two National Dex drafts, you would put 2. If you will have a National Dex draft and a Galar Dex draft, you would put 2.',
            'allows_cross_subleague_matches': 'Will players in different subleagues potentially play each other in the regular season or playoffs?',
            'teambased': 'Will coaches belong to a larger team of coaches that collectively competes against other teams (Similar to Smogon Premier League)?',
        }

class SubleagueConfigurationForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))

    class Meta:
        model = subleague
        fields = ['name']
        labels = {
            'name': 'Subleague Name',
        }

class TierForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary btn-sm'))

    class Meta:
        model = league_tier
        fields = ['tier','points']
        labels = {
            'tier': 'Tier Name',
            'points': 'Points',
        }
    
    def __init__(self, *args, **kwargs):
        super(TierForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-sm'

class RulesForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary btn-sm form-control'))

    class Meta:
        model = rules
        fields = ['rules']
        labels = {
            'rules': 'Rules',
        }

class SeasonConfigurationForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))

    class Meta:
        model = season
        fields = ['name','draftstart','drafttimer','draftbudget', 'picksperteam','drafttype', 'seasonstart','seasonlength', 'playoffslength', 'freeagenciesallowed','tradesallowed']
        labels = {
            'name': 'Season Name',
            'draftstart': 'When does the draft start?',
            'drafttimer': 'How long is the draft timer in hours?',
            'draftbudget': 'What is the total draft budget coaches will have?', 
            'picksperteam': 'How many Pokemon can each team draft?',
            'drafttype': 'How does draft order proceed at the end of a round?', 
            'seasonstart': 'When does the season start?',
            'seasonlength': 'How many weeks is the regular season?', 
            'playoffslength': 'How many weeks of playoffs will there be?', 
            'freeagenciesallowed': 'How many free agencies per team will be allowed?',
            'tradesallowed': 'How many trades per team will be allowed?',
        }

        help_texts = {
            'draftstart': 'Use the following format (UTC Timezone): YYYY-MM-DD HH:MM',
            'seasonstart': 'Use the following format (UTC Timezone): YYYY-MM-DD HH:MM',
        }

class ConferenceForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Add Conference', css_class='btn-primary btn-sm form-control'))
    helper.form_show_labels = False

    class Meta:
        model = conference
        fields = ['conference']
        labels = {
            'conference': 'Conference Name',
        }

class DivisionForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Add Division', css_class='btn-primary btn-sm form-control'))
    helper.form_show_labels = False

    class Meta:
        model = division
        fields = ['division']
        labels = {
            'division': 'Division Name',
        }
    
