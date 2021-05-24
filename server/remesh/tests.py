from django.test import TestCase
from django.urls import reverse
from .models import Team, Conversation
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.messages import get_messages
import datetime


def create_user(client):
  user = User.objects.create_user(username='testuser', password='12345')
  login = client.login(username='testuser', password='12345')
  return user, login


def create_team(user):
  t = Team.objects.create()
  t.members.set([user])
  return t


class TeamIndexViewTests(TestCase):
  def test_no_teams(self):
    user, login = create_user(self.client)
    response = self.client.get(reverse('remesh:team_index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No teams are available.")
    self.assertQuerysetEqual(response.context['team_list'], [])

  def test_shows_teams(self):
    user, login = create_user(self.client)
    team1 = create_team(user=user)
    response = self.client.get(reverse('remesh:team_index'))
    self.assertEqual(response.status_code, 200)
    self.assertNotContains(response, "No teams are available.")
    self.assertQuerysetEqual(response.context['team_list'], [team1])

class TeamDetailViewTests(TestCase):
  def test_no_team_details_404(self):
    user, login = create_user(self.client)
    response = self.client.get(reverse('remesh:team_detail', args=(1,)))
    self.assertEqual(response.status_code, 404)

  def test_shows_team_details(self):
    user, login = create_user(self.client)
    team1 = create_team(user=user)
    response = self.client.get(reverse('remesh:team_detail', args=(team1.id,)))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['team'], team1)

class TeamAddFormTests(TestCase):
  def test_add_team_form_exists(self):
    user, login = create_user(self.client)
    response = self.client.get(reverse('remesh:team_add'))
    self.assertEqual(response.status_code, 200)
    labels = [
        'Members',
        'Submit']
    for label in labels:
      self.assertContains(response, label)

  def test_add_team_form_post_for_valid_data(self):
    user, login = create_user(self.client)
    response = self.client.post(
      reverse('remesh:team_add'),
      data={
        'members': ['1']
      }
    )
    self.assertRedirects(response, reverse('remesh:team_add'))
    self.assertEqual(response.status_code, 302)
    c = Team.objects.all().count()
    self.assertEqual(c, 1)

class TeamEditFormTests(TestCase):
  def test_edit_team_form_404_with_invalid_team_id(self):
    user, login = create_user(self.client)
    response = self.client.get(reverse('remesh:team_edit', args=(1,)))
    self.assertEqual(response.status_code, 404)

  def test_edit_team_form_post_for_valid_data(self):
    user, login = create_user(self.client)
    team1 = create_team(user=user)
    response = self.client.post(
      reverse('remesh:team_edit', args=(1,)),
      data={
        'members': ['1']
      }
    )
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse('remesh:team_index'))
    c = Team.objects.all().count()
    self.assertEqual(c, 1)