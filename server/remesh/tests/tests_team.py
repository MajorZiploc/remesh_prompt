from django.test import TestCase
from django.urls import reverse
from remesh.models import Team
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.messages import get_messages
from .utils_for_tests import *


class TeamIndexViewTests(TestCase):
  def test_no_teams(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    login = self.client.login(username=username, password=password)
    response = self.client.get(reverse('remesh:team_index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No teams are available.")
    self.assertContains(response, '<a id="add-team"')
    self.assertNotContains(response, '<a id="team-list-item-')
    self.assertQuerysetEqual(response.context['team_list'], [])

  def test_shows_teams(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    login = self.client.login(username=username, password=password)
    team1 = create_team(name="foodies", users=[user])
    team2 = create_team(name="show lovers", users=[user])
    response = self.client.get(reverse('remesh:team_index'))
    self.assertEqual(response.status_code, 200)
    self.assertNotContains(response, "No teams are available.")
    self.assertContains(response, '<a id="add-team"')
    self.assertQuerysetEqual(response.context['team_list'], [team1, team2])
    for i in ['0', '1']:
      self.assertContains(response, '<a id="team-list-item-' + i)


class TeamDetailViewTests(TestCase):
  def test_no_team_details_404(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    login = self.client.login(username=username, password=password)
    response = self.client.get(reverse('remesh:team_detail', args=(1,)))
    self.assertEqual(response.status_code, 404)

  def test_shows_team_details(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    login = self.client.login(username=username, password=password)
    team1 = create_team(name="foodies", users=[user])
    response = self.client.get(reverse('remesh:team_detail', args=(team1.pk,)))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['team'], team1)
    self.assertContains(response, "<a id='edit-team'")
    self.assertContains(response, "<a id='goto-conversations'")


class TeamAddFormTests(TestCase):
  def test_add_team_form_exists(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    login = self.client.login(username=username, password=password)
    response = self.client.get(reverse('remesh:team_add'))
    self.assertEqual(response.status_code, 200)
    labels = [
        'Name',
        'Members',
        'Submit']
    for label in labels:
      self.assertContains(response, label)

  def test_add_team_form_post_for_valid_data(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    login = self.client.login(username=username, password=password)
    response = self.client.post(
      reverse('remesh:team_add'),
      data={
        'name': 'foodies',
        'members': ['1']
      }
    )
    self.assertRedirects(response, reverse('remesh:team_index'))
    self.assertEqual(response.status_code, 302)
    c = Team.objects.all().count()
    self.assertEqual(c, 1)


class TeamEditFormTests(TestCase):
  def test_edit_team_form_404_with_invalid_team_id(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    login = self.client.login(username=username, password=password)
    response = self.client.get(reverse('remesh:team_edit', args=(1,)))
    self.assertEqual(response.status_code, 404)

  def test_edit_team_form_post_for_valid_data(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    login = self.client.login(username=username, password=password)
    team1 = create_team(name="foodies", users=[user])
    response = self.client.post(
      reverse('remesh:team_edit', args=(team1.pk,)),
      data={
        'name': 'foodies',
        'members': ['1']
      }
    )
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse('remesh:team_index'))
    c = Team.objects.all().count()
    self.assertEqual(c, 1)


class TeamDeleteFormTests(TestCase):
  def test_delete_team_form_post_for_valid_data_deletes_the_correct_team(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    login = self.client.login(username=username, password=password)
    team1 = create_team(name="foodies", users=[user])
    team2 = create_team(name="shoe lovers", users=[user])
    response = self.client.post(reverse('remesh:team_delete', args=(team1.pk,)))
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse('remesh:team_index'))
    self.assertEqual(list(Team.objects.all()), [team2])
