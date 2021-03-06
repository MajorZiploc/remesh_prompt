from django import forms

from .models import Conversation, Message, Thought


class ConversationForm(forms.ModelForm):
  class Meta:
    model = Conversation
    fields = "__all__"


class ThoughtForm(forms.ModelForm):
  class Meta:
    model = Thought
    exclude = ['message']


class MessageForm(forms.ModelForm):
  class Meta:
    model = Message
    exclude = ['conversation']
