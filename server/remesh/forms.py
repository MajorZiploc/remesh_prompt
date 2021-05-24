from django import forms

from .models import Team, Conversation

class TeamForm(forms.ModelForm):
  class Meta:
    model = Team
    fields = "__all__"


class ConversationForm(forms.ModelForm):
  class Meta:
    model = Conversation
    fields = "__all__"
