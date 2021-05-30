from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse, reverse_lazy
from remesh.models import Conversation
from django.utils import timezone
from remesh.forms import ConversationForm


class ConversationIndexView(generic.ListView):
  template_name = 'remesh/conversation_index.html'
  context_object_name = 'conversation_list'

  def get_queryset(self, *args, **kwargs):
    search_phrase = self.request.GET.get('search_phrase', None)
    if (search_phrase):
      return Conversation.objects.filter(title__icontains=search_phrase)
    return Conversation.objects.all()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Conversations'
    return context


class ConversationAddView(generic.FormView):
  form_class = ConversationForm
  template_name = 'remesh/add.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Conversation'
    return context

  def get_success_url(self):
    return reverse('remesh:conversation_index')

  def get_initial(self):
    initial = super().get_initial()
    return initial

  def form_valid(self, form):
    form.save()
    return super().form_valid(form)
