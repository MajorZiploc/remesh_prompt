from django.test import TestCase
from django.urls import reverse
from remesh.views import ConversationIndexView
from remesh.models import Conversation
from django.contrib.messages import get_messages
from .utils_for_tests import *
from django.utils import timezone
from datetime import timedelta


class ConversationModelTests(TestCase):
  def test_is_active(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    team1 = create_team(name="foodies", users=[user])
    now = timezone.now()
    start_time = now - timedelta(minutes=60)
    conversation = create_conversation(
      moderator=user, team=team1,
      start_date_time=start_time,
      duration=timedelta(minutes=120))
    self.assertTrue(conversation.is_active())

  def test_is_not_active_past(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    team1 = create_team(name="foodies", users=[user])
    now = timezone.now()
    start_time = now - timedelta(minutes=121)
    conversation = create_conversation(
      moderator=user, team=team1,
      start_date_time=start_time,
      duration=timedelta(minutes=120))
    self.assertFalse(conversation.is_active())

  def test_is_not_active_future(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    team1 = create_team(name="foodies", users=[user])
    now = timezone.now()
    start_time = now + timedelta(minutes=121)
    conversation = create_conversation(
      moderator=user, team=team1,
      start_date_time=start_time,
      duration=timedelta(minutes=120))
    self.assertFalse(conversation.is_active())

  def test_is_not_active_future_starting_soon(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    team1 = create_team(name="foodies", users=[user])
    now = timezone.now()
    start_time = now + timedelta(minutes=1)
    conversation = create_conversation(
      moderator=user, team=team1,
      start_date_time=start_time,
      duration=timedelta(minutes=2))
    self.assertFalse(conversation.is_active())


class ConversationIndexViewTests(TestCase):
  def test_no_conversations(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    team1 = create_team(name="foodies", users=[user])
    login = self.client.login(username=username, password=password)
    response = self.client.get(reverse('remesh:team_conversation_index', args=(team1.pk,)))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No conversations are available.")
    # self.assertContains(response, "Add New Conversation")
    self.assertQuerysetEqual(response.context['conversation_list'], [])

  def test_conversation_is_in_index(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    team1 = create_team(name="foodies", users=[user])
    login = self.client.login(username=username, password=password)
    conversation = create_conversation(moderator=user, team=team1)
    response = self.client.get(reverse('remesh:team_conversation_index', args=(conversation.pk,)))
    self.assertEqual(response.status_code, 200)
    self.assertNotContains(response, "No conversations are available.")
    self.assertContains(response, "All Conversations")
    # self.assertContains(response, "Add New Conversation")
    self.assertQuerysetEqual(response.context['conversation_list'], [conversation])


class ConversationActiveViewTests(TestCase):
  def test_no_conversations(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    team1 = create_team(name="foodies", users=[user])
    login = self.client.login(username=username, password=password)
    response = self.client.get(reverse('remesh:team_conversation_active', args=(team1.pk,)))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No conversations are available.")
    # self.assertContains(response, "Add New Conversation")
    self.assertQuerysetEqual(response.context['conversation_list'], [])

  def test_conversation_is_in_active(self):
    username, password = get_user_creds()
    user = create_user(username, password)
    team1 = create_team(name="foodies", users=[user])
    team2 = create_team(name="foodies2", users=[user])
    login = self.client.login(username=username, password=password)
    conversation1 = create_conversation(
        title='Pancakes',
        moderator=user,
        team=team1,
        start_date_time=timezone.now() -
        timedelta(
            minutes=10),
        duration=timedelta(
            minutes=20))
    conversation2 = create_conversation(
        title='Tuna dishes',
        moderator=user,
        team=team1,
        start_date_time=timezone.now() -
        timedelta(
            minutes=40),
        duration=timedelta(
            minutes=143))
    conversation3 = create_conversation(
        title='ZTuna dishes',
        moderator=user,
        team=team1,
        start_date_time=timezone.now() -
        timedelta(
            minutes=40),
        duration=timedelta(
            minutes=5))
    conversation4 = create_conversation(
        title='zPancakes',
        moderator=user,
        team=team2,
        start_date_time=timezone.now() -
        timedelta(
            minutes=50),
        duration=timedelta(
            minutes=20))
    response = self.client.get(reverse('remesh:team_conversation_active', args=(conversation1.pk,)))
    self.assertEqual(response.status_code, 200)
    self.assertNotContains(response, "No conversations are available.")
    self.assertContains(response, "Active Conversations")
    self.assertQuerysetEqual(response.context['conversation_list'], [conversation1, conversation2])


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
    team1 = create_team(name="foodies", users=[user])
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
    team1 = create_team(name="foodies", users=[user])
    login = self.client.login(username=username, password=password)
    response = self.client.get(reverse('remesh:conversation_add', args=(team1.pk,)))
    self.assertEqual(response.status_code, 200)
    labels = [
        'Title',
        'Start date time',
        'Duration',
        'Max num of participants',
        'Moderator',
        'Submit']
    for label in labels:
      self.assertContains(response, label)

  # def test_add_conversation_form_post_for_valid_data(self):
  #   username, password = get_user_creds()
  #   user = create_user(username, password)
  #   team1 = create_team(name="foodies", users=[user])
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
  #   team1 = create_team(name="foodies", users=[user])
  #   conversation1 = create_conversation(moderator=user, team=team1)
  #   login = self.client.login(username=username, password=password)
  #   response = self.client.post(
  #     reverse('remesh:conversation_edit', args=(conversation1.pk,)),
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
