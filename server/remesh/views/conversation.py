from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse, reverse_lazy
from remesh.models import Conversation, Team
from django.utils import timezone
from remesh.forms import TeamForm, ConversationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()


class ConversationIndexView(LoginRequiredMixin, generic.ListView):
  template_name = 'remesh/team_conversation_index.html'
  context_object_name = 'conversation_list'

  def get_queryset(self, *args, **kwargs):
    return Conversation.objects.filter(team__pk=self.kwargs['team_pk'])

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'All Conversations'
    return context


class ConversationActiveView(LoginRequiredMixin, generic.ListView):
  template_name = 'remesh/team_conversation_index.html'
  context_object_name = 'conversation_list'

  def get_queryset(self, *args, **kwargs):
    return [conv for conv in Conversation.objects
            .filter(team__pk=self.kwargs['team_pk']) if conv.is_active()]

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Active Conversations'
    return context


class ConversationPastView(LoginRequiredMixin, generic.ListView):
  template_name = 'remesh/team_conversation_past.html'
  context_object_name = 'conversation_list'

  def get_queryset(self, *args, **kwargs):
    return [conv for conv in Conversation.objects
            .filter(team__pk=self.kwargs['team_pk']) if conv.is_past()]

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Past Conversations'
    return context


class ConversationFutureView(LoginRequiredMixin, generic.ListView):
  template_name = 'remesh/team_conversation_future.html'
  context_object_name = 'conversation_list'

  def get_queryset(self, *args, **kwargs):
    return [conv for conv in Conversation.objects
            .filter(team__pk=self.kwargs['team_pk']) if conv.is_future()]

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Future Conversations'
    return context


class ConversationDetailView(LoginRequiredMixin, generic.DetailView):
  model = Conversation
  template_name = 'remesh/conversation_detail.html'


class ConversationAddView(LoginRequiredMixin, generic.FormView):
  form_class = ConversationForm
  template_name = 'remesh/conversation_add.html'

  def get_success_url(self):
    return reverse('remesh:team_conversation_index', args=(self.kwargs['pk'],))

  def get_initial(self):
    initial = super().get_initial()
    # if self.request.user.is_authenticated:
    # initial.update({'name': self.request.user.get_full_name()})
    return initial

  def form_valid(self, form):
    form = ConversationForm(self.request.POST)
    conversation = form.save(commit=False)
    conversation.team__pk = self.kwargs['team_id']
    conversation.save()
    return super().form_valid(form)


class ConversationEditView(LoginRequiredMixin, generic.UpdateView):
  form_class = ConversationForm
  template_name = 'remesh/conversation_edit.html'

  def get_success_url(self):
    return reverse('remesh:team_conversation_index', args=(self.kwargs['pk'],))

  def get_initial(self):
    initial = super().get_initial()
    # if self.request.user.is_authenticated:
    # initial.update({'name': self.request.user.get_full_name()})
    return initial

  def get_object(self, *args, **kwargs):
    conversation = get_object_or_404(Conversation, pk=self.kwargs['pk'])
    return conversation

  def form_valid(self, form):
    form.save()
    return super().form_valid(form)
