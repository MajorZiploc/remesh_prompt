from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse, reverse_lazy
from .models import Conversation, Team
from django.utils import timezone
from .forms import TeamForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()


class TeamIndexView(LoginRequiredMixin, generic.ListView):
  template_name = 'remesh/team_index.html'
  context_object_name = 'team_list'

  def get_queryset(self):
    return Team.objects.all()


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
  model = Team
  template_name = 'remesh/team_detail.html'

class TeamAddView(LoginRequiredMixin, generic.FormView):
  form_class = TeamForm
  template_name = 'remesh/team_add.html'
  success_url = reverse_lazy('remesh:team_index')

  def get_initial(self):
    initial = super().get_initial()
    # if self.request.user.is_authenticated:
    # initial.update({'name': self.request.user.get_full_name()})
    return initial

  def form_valid(self, form):
    form.save()
    return super().form_valid(form)

class TeamEditView(LoginRequiredMixin, generic.UpdateView):
  form_class = TeamForm
  template_name = 'remesh/team_edit.html'
  success_url = reverse_lazy('remesh:team_index')

  def get_initial(self):
    initial = super().get_initial()
    # if self.request.user.is_authenticated:
    # initial.update({'name': self.request.user.get_full_name()})
    return initial

  def get_object(self, *args, **kwargs):
    team = get_object_or_404(Team, pk=self.kwargs['pk'])
    return team

  def form_valid(self, form):
    form.save()
    return super().form_valid(form)

class ConversationIndexView(LoginRequiredMixin, generic.ListView):
  template_name = 'remesh/conversation_index.html'
  context_object_name = 'conversation_list'

  def get_queryset(self, *args, **kwargs):
    return Conversation.objects.filter(team__pk=self.kwargs['team_pk'])
