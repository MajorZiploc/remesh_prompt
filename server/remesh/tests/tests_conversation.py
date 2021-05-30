from django.test import TestCase
from django.urls import reverse
from remesh.views import ConversationIndexView
from remesh.models import Conversation
from django.contrib.messages import get_messages
from .utils_for_tests import *
from django.utils import timezone
from datetime import timedelta


class ConversationIndexViewTests(TestCase):
  def test_no_conversations(self):
    response = self.client.get(reverse('remesh:conversation_index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No conversations are available.")
    self.assertContains(response, "Add New Conversation")
    self.assertQuerysetEqual(response.context['conversation_list'], [])

  def test_conversation_is_in_index(self):
    conversation = create_conversation()
    conversation2 = create_conversation(title='Tacos')
    response = self.client.get(reverse('remesh:conversation_index'))
    self.assertEqual(response.status_code, 200)
    self.assertNotContains(response, "No conversations are available.")
    self.assertContains(response, "Conversations")
    self.assertContains(response, "Add New Conversation")
    self.assertQuerysetEqual(response.context['conversation_list'], [conversation, conversation2])


class ConversationAddFormTests(TestCase):
  def test_add_conversation_form_exists(self):
    response = self.client.get(reverse('remesh:conversation_add'))
    self.assertEqual(response.status_code, 200)
    labels = [
        'Title',
        'Start date time',
        'Submit']
    for label in labels:
      self.assertContains(response, label)

  def test_add_conversation_form_post_for_valid_data(self):
    response = self.client.post(
      reverse('remesh:conversation_add'),
      data={
        'title': 'Pancakes',
        'start_date_time': "01/01/2020",
      }
    )
    self.assertRedirects(response, reverse('remesh:conversation_index'))
    c = Conversation.objects.all().count()
    self.assertEqual(c, 1)
