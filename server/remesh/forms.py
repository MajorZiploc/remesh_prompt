from django import forms

from .models import Day, Team


class DayForm(forms.ModelForm):
  class Meta:
    model = Day
    fields = "__all__"

class TeamForm(forms.ModelForm):
  class Meta:
    model = Team
    fields = "__all__"
