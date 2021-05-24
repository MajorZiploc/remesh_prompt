from django.shortcuts import render
from django.views import generic
from django.urls import reverse, reverse_lazy
from .models import Day, WeightUnit
from django.utils import timezone
from .forms import DayForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()


class AddDayView(LoginRequiredMixin, generic.FormView):
  form_class = DayForm
  template_name = 'body_comp/add_day.html'
  success_url = reverse_lazy('body_comp:add_day')

  def get_initial(self):
    initial = super().get_initial()
    # if self.request.user.is_authenticated:
    # initial.update({'name': self.request.user.get_full_name()})
    return initial

  def form_valid(self, form):
    form.save()
    return super().form_valid(form)


class IndexView(LoginRequiredMixin, generic.ListView):
  template_name = 'body_comp/index.html'
  context_object_name = 'day_list'

  def get_queryset(self):
    """
    """
    return Day.objects.filter(
        day_date__lte=timezone.now()
    ).order_by('-day_date')[:]


class DetailView(LoginRequiredMixin, generic.DetailView):
  model = Day
  template_name = 'body_comp/detail.html'
