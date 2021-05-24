from django.test import TestCase
from django.urls import reverse
from .models import Day, WeightUnit
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.messages import get_messages
import datetime


def create_user(client):
  user = User.objects.create_user(username='testuser', password='12345')
  login = client.login(username='testuser', password='12345')
  return user, login


def create_weight_units() -> WeightUnit:
  return WeightUnit.objects.create(name='Pounds', label='lbs')


def create_day(days, user):
  time = timezone.now() + datetime.timedelta(days=days)
  w = WeightUnit.objects.get(name='Pounds')
  return w.day_set.create(day_date=time, fit_user=user)


class DayIndexViewTests(TestCase):
  def test_no_days(self):
    """
    If no days exist, an appropriate message is displayed.
    """
    user, login = create_user(self.client)
    response = self.client.get(reverse('body_comp:index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No days are available.")
    self.assertQuerysetEqual(response.context['day_list'], [])

  def test_shows_day(self):
    """
    Shows day
    """
    user, login = create_user(self.client)
    create_weight_units()
    day1 = create_day(days=-30, user=user)
    response = self.client.get(reverse('body_comp:index'))
    self.assertEqual(response.status_code, 200)
    self.assertNotContains(response, "No days are available.")
    self.assertQuerysetEqual(response.context['day_list'], [day1])


class DayDetailViewTests(TestCase):
  def test_no_day_details_404(self):
    user, login = create_user(self.client)
    create_weight_units()
    response = self.client.get(reverse('body_comp:detail', args=(1,)))
    self.assertEqual(response.status_code, 404)

  def test_shows_day_details(self):
    """
    Shows day
    """
    user, login = create_user(self.client)
    create_weight_units()
    day1 = create_day(days=-30, user=user)
    response = self.client.get(reverse('body_comp:detail', args=(day1.id,)))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['day'], day1)


class AddDayFormTests(TestCase):
  def test_add_day_form_exists(self):
    user, login = create_user(self.client)
    response = self.client.get(reverse('body_comp:add_day'))
    self.assertEqual(response.status_code, 200)
    labels = [
        'Submit',
        'Weight units',
        'Calories',
        'Morning weight',
        'Body fat percentage',
        'Muscle mass percentage',
        'Day date']
    for label in labels:
      self.assertContains(response, label)

  def test_add_day_form_post_for_invalid_date(self):
    user, login = create_user(self.client)
    wu = create_weight_units()
    response = self.client.post(
      reverse('body_comp:add_day'),
      data={'weight_units': wu.pk, 'day_date': 'fdsa'}
    )
    self.assertEqual(response.status_code, 200)
    labels = ['Enter a valid date.']
    for label in labels:
      self.assertContains(response, label)

  def test_add_day_form_post_for_valid_data(self):
    user, login = create_user(self.client)
    wu = create_weight_units()
    response = self.client.post(
      reverse('body_comp:add_day'),
      data={
        'weight_units': wu.pk,
        'day_date': '06/06/2020',
        'calories': 2500,
        'morning_weight': 144,
        'body_fat_percentage': 15,
        'muscle_mass_percentage': 45,
        'fit_user': user.pk
      }
    )
    self.assertRedirects(response, reverse('body_comp:add_day'))
    self.assertEqual(response.status_code, 302)
    c = Day.objects.filter(calories=2500).count()
    self.assertEqual(c, 1)
