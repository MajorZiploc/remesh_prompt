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
    # self.assertContains(response, "Add New Conversation")
    self.assertQuerysetEqual(response.context['conversation_list'], [])

  def test_conversation_is_in_index(self):
    conversation = create_conversation()
    response = self.client.get(reverse('remesh:conversation_index'))
    self.assertEqual(response.status_code, 200)
    self.assertNotContains(response, "No conversations are available.")
    self.assertContains(response, "All Conversations")
    # self.assertContains(response, "Add New Conversation")
    self.assertQuerysetEqual(response.context['conversation_list'], [conversation])


class ConversationDetailViewTests(TestCase):
  def test_no_conversation_details_404(self):
    response = self.client.get(reverse('remesh:conversation_detail', args=(1,)))
    self.assertEqual(response.status_code, 404)

  def test_shows_conversation_details(self):
    conversation1 = create_conversation()
    response = self.client.get(reverse('remesh:conversation_detail', args=(conversation1.pk,)))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['conversation'], conversation1)
    self.assertContains(response, 'Edit this conversation')
    self.assertContains(response, "<a id='edit-conversation'")


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


class ConversationEditFormTests(TestCase):
  def test_edit_conversation_form_404_with_invalid_conversation_id(self):
    response = self.client.get(reverse('remesh:conversation_edit', args=(1,)))
    self.assertEqual(response.status_code, 404)

  def test_edit_conversation_form_post_for_valid_data(self):
    conversation1 = create_conversation(title='Pancakes')
    response = self.client.post(
      reverse('remesh:conversation_edit', args=(conversation1.pk,)),
      data={
        'moderator': '1',
        'title': 'Candy Worms',
        'start_date_time': "01/01/2020",
        'duration': '60',
        'max_num_of_participants': '40'
      }
    )
    self.assertEqual(response.status_code, 302)
    self.assertRedirects(response, reverse('remesh:conversation_index'))
    c = Conversation.objects.all().count()
    self.assertEqual(c, 1)
    conv = Conversation.objects.get(pk=conversation1.pk)
    self.assertEqual(conv.title, 'Candy Worms')
