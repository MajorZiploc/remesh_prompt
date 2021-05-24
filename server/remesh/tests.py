from django.test import TestCase
from django.urls import reverse
from remesh.views import ConversationIndexView
from .models import Team, Conversation
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.messages import get_messages
from datetime import datetime, timedelta


def create_user(username, password):
  user = User.objects.create_user(username=username, password=password)
  return user


def get_user_creds():
  return 'testuser', '12345'


def create_team(user):
  t = Team.objects.create()
  t.members.set([user])
  return t


def create_conversation(moderator, team):
  return Conversation.objects.create(
      title='Pancakes',
      date=datetime.now(),
      start_time=datetime.now(),
      duration=timedelta(
          days=2),
      max_num_of_participants=50,
      moderator=moderator,
      team=team)


class TeamIndexViewTests(TestCase):
  def test_no_teams(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    login = self.client.login(username=username, password=password)
    response = self.client.get(reverse('remesh:team_index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No teams are available.")
    self.assertContains(response, "Add New Team")
    self.assertQuerysetEqual(response.context['team_list'], [])

  def test_shows_teams(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    login = self.client.login(username=username, password=password)
    team1 = create_team(user=user)
    response = self.client.get(reverse('remesh:team_index'))
    self.assertEqual(response.status_code, 200)
    self.assertNotContains(response, "No teams are available.")
    self.assertContains(response, "Add New Team")
    self.assertQuerysetEqual(response.context['team_list'], [team1])


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
    team1 = create_team(user=user)
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


class ConversationIndexViewTests(TestCase):
  def test_no_conversations(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    team1 = create_team(user=user)
    login = self.client.login(username=username, password=password)
    response = self.client.get(reverse('remesh:conversation_index', args=(1,)))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No conversations are available.")
    # self.assertContains(response, "Add New Conversation")
    self.assertQuerysetEqual(response.context['conversation_list'], [])

  def test_conversation_is_in_index(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    team1 = create_team(user=user)
    login = self.client.login(username=username, password=password)
    conversation = create_conversation(moderator=user, team=team1)
    response = self.client.get(reverse('remesh:conversation_index', args=(conversation.pk,)))
    self.assertEqual(response.status_code, 200)
    self.assertNotContains(response, "No conversations are available.")
    # self.assertContains(response, "Add New Conversation")
    self.assertQuerysetEqual(response.context['conversation_list'], [conversation])


class ConversationDetailViewTests(TestCase):
  def test_no_conversation_details_404(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    login = self.client.login(username=username, password=password)
    response = self.client.get(reverse('remesh:conversation_detail', args=(1,)))
    self.assertEqual(response.status_code, 404)

  def test_shows_conversation_details(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    team1 = create_team(user=user)
    conversation1 = create_conversation(moderator=user, team=team1)
    login = self.client.login(username=username, password=password)
    response = self.client.get(reverse('remesh:conversation_detail', args=(conversation1.pk,)))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['conversation'], conversation1)
    self.assertContains(response, 'Edit this conversation')
    self.assertContains(response, "<a id='edit-conversation'")


class ConversationAddFormTests(TestCase):
  def test_add_conversation_form_exists(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    login = self.client.login(username=username, password=password)
    response = self.client.get(reverse('remesh:conversation_add'))
    self.assertEqual(response.status_code, 200)
    labels = [
        'Title',
        'Date',
        'Start time',
        'Duration',
        'Max num of participants',
        'Moderator',
        'Team',
        'Submit']
    for label in labels:
      self.assertContains(response, label)

  # def test_add_conversation_form_post_for_valid_data(self):
  #   username, password = get_user_creds()
  #   user = create_user(username, password)
  #   team1 = create_team(user=user)
  #   login = self.client.login(username=username, password=password)
  #   response = self.client.post(
  #     reverse('remesh:conversation_add'),
  #     data={
  #       'moderator': ['1'],
  #       'team': ['1'],
  #       'title': 'Pancakes',
  #       'date': "2020-05-24",
  #       'duration': '60',
  #       'max_num_of_participants': '40'
  #     }
  #   )
  #   self.assertRedirects(response, reverse('remesh:team_index'))
  #   self.assertEqual(response.status_code, 302)
  #   c = Conversation.objects.all().count()
  #   self.assertEqual(c, 1)


class ConversationEditFormTests(TestCase):
  def test_edit_conversation_form_404_with_invalid_conversation_id(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    login = self.client.login(username=username, password=password)
    response = self.client.get(reverse('remesh:conversation_edit', args=(1,)))
    self.assertEqual(response.status_code, 404)

  # def test_edit_conversation_form_post_for_valid_data(self):
  #   username, password = get_user_creds()
  #   user = create_user(username, password)
  #   team1 = create_team(user=user)
  #   conversation1 = create_conversation(moderator=user, team=team1)
  #   login = self.client.login(username=username, password=password)
  #   response = self.client.post(
  #     reverse('remesh:conversation_edit', args=(1,)),
  #     data={
  #       'moderator': ['1'],
  #       'team': ['1'],
  #       'title': 'Pancakes',
  #       'date': "2020-05-24",
  #       'duration': '60',
  #       'max_num_of_participants': '40'
  #     }
  #   )
  #   self.assertEqual(response.status_code, 302)
  #   self.assertRedirects(response, reverse('remesh:team_index'))
  #   c = Conversation.objects.all().count()
  #   self.assertEqual(c, 1)
