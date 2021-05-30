from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse, reverse_lazy
from remesh.models import Thought, Message
from django.utils import timezone
from remesh.forms import ThoughtForm


class ThoughtIndexView(generic.ListView):
  template_name = 'remesh/thought_index.html'
  context_object_name = 'thought_list'

  def get_queryset(self, *args, **kwargs):
    return Thought.objects.filter(message__pk=self.kwargs['message_pk'])

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['message_pk'] = self.kwargs['message_pk']
    message = Message.objects.get(pk=self.kwargs['message_pk'])
    context['message'] = message
    context['title'] = f'Thoughts on the message: "{message.text}"'
    return context


class ThoughtAddView(generic.FormView):
  form_class = ThoughtForm
  template_name = 'remesh/add.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = 'Thought'
    return context

  def get_success_url(self):
    return reverse('remesh:thought_index', args=(self.kwargs['message_pk'],))

  def get_initial(self):
    initial = super().get_initial()
    return initial

  def form_valid(self, form):
    thought = Thought(message=Message.objects.get(pk=self.kwargs['message_pk']))
    form = ThoughtForm(self.request.POST, instance=thought)
    form.save()
    return super().form_valid(form)
