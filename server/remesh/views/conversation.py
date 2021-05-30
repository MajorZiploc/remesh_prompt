from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse, reverse_lazy
from remesh.models import Conversation
from django.utils import timezone
from remesh.forms import ConversationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()


class ConversationIndexView(LoginRequiredMixin, generic.ListView):
  template_name = 'remesh/conversation_index.html'
  context_object_name = 'conversation_list'

  def get_queryset(self, *args, **kwargs):
    return Conversation.objects.all()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'All Conversations'
    return context


class ConversationDetailView(LoginRequiredMixin, generic.DetailView):
  model = Conversation
  template_name = 'remesh/conversation_detail.html'


class ConversationAddView(LoginRequiredMixin, generic.FormView):
  form_class = ConversationForm
  template_name = 'remesh/conversation_add.html'

  def get_success_url(self):
    return reverse('remesh:conversation_index')

  def get_initial(self):
    initial = super().get_initial()
    return initial

  def form_valid(self, form):
    form.save()
    return super().form_valid(form)


class ConversationEditView(LoginRequiredMixin, generic.UpdateView):
  form_class = ConversationForm
  template_name = 'remesh/conversation_edit.html'

  def get_success_url(self):
    return reverse('remesh:conversation_index')

  def get_initial(self):
    initial = super().get_initial()
    return initial

  def get_object(self, *args, **kwargs):
    conversation = get_object_or_404(Conversation, pk=self.kwargs['pk'])
    return conversation

  def form_valid(self, form):
    form.save()
    return super().form_valid(form)
