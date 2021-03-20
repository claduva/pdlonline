from django import forms
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from .models import league, league_configuration, subleague
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

class CreateLeagueForm(forms.ModelForm):
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Next', css_class='btn-primary'))

    class Meta:
        model = league
        fields = ['name','abbreviation','logo','platform','discordserver','discordurl']
        labels = {
            'name': 'League Name',
            'abbreviation': 'League Abbreviation',
            'discordserver': 'Discord Server Name',
            'discordurl': 'Discord Invite URL',
        }
        help_texts = {
            'name': 'e.g. All Star Premier League',
            'abbreviation': 'e.g. ASPL',
            'logo': 'Try uploading image to Discord, right-clicking, and selecting "Copy Image Address"',
            'discordserver': 'This is the server name of your Discord server',
            'discordurl': 'This is an invite link to your league\'s Discord server',
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