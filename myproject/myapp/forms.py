from django import forms
from .models import Player, Team  # Make sure Team is imported here
from .models import PlayerStats  # Make sure you have this model created
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'age', 'team', 'position']

    team = forms.ModelChoiceField(queryset=Team.objects.all(), empty_label="Select a Team")


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', 'team_logo']
class ScheduleForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
class PlayerStatsForm(forms.ModelForm):
    class Meta:
        model = PlayerStats
        fields = ['role', 'runs', 'wickets']
