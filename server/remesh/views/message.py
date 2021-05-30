from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse, reverse_lazy
from remesh.models import Conversation, Message
from django.utils import timezone
from remesh.forms import MessageForm


class MessageIndexView(generic.ListView):
  template_name = 'remesh/message_index.html'
  context_object_name = 'message_list'

  def get_queryset(self, *args, **kwargs):
    search_phrase = self.request.GET.get('search_phrase', None)
    if (search_phrase):
      return Message.objects.filter(conversation__pk=self.kwargs['conversation_pk']).filter(text__icontains=search_phrase)
    return Message.objects.filter(conversation__pk=self.kwargs['conversation_pk'])

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    search_phrase = self.request.GET.get('search_phrase', None)
    if (search_phrase):
      context['title'] = f'Messages that contain {search_phrase}'
    else:
      context['title'] = 'All Messages'
    context['conversation_pk'] = self.kwargs['conversation_pk']
    return context


class MessageAddView(generic.FormView):
  form_class = MessageForm
  template_name = 'remesh/add.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Message'
    return context

  def get_success_url(self):
    return reverse('remesh:message_index', args=(self.kwargs['conversation_pk'],))

  def get_initial(self):
    initial = super().get_initial()
    return initial

  def form_valid(self, form):
    message = Message(conversation=Conversation.objects.get(pk=self.kwargs['conversation_pk']))
    form = MessageForm(self.request.POST, instance=message)
    form.save()
    return super().form_valid(form)
