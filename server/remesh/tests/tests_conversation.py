from django.test import TestCase
from django.urls import reverse
from remesh.models import Conversation
from .utils_for_tests import *
from django.utils import timezone
from datetime import timedelta


class ConversationIndexViewTests(TestCase):
  def test_no_conversations_empty_index(self):
    response = self.client.get(reverse('remesh:conversation_index'))
    self.assertEqual(response.status_code, 200)
    self.assertNotContains(response, "All Conversations")
    self.assertNotContains(response, "Conversations that contain")
    self.assertContains(response, "No conversations are available.")
    self.assertContains(response, "Add New Conversation")
    self.assertQuerysetEqual(response.context['conversation_list'], [])

  def test_conversations_are_in_index_with_proper_order(self):
    conversation = create_conversation(title='Pancakes', start_date_time=(timezone.now() - timedelta(days=1)))
    conversation2 = create_conversation(title='Tacos', start_date_time=(timezone.now() - timedelta(days=0)))
    conversation3 = create_conversation(title='ZTacos', start_date_time=(timezone.now() - timedelta(days=100)))
    response = self.client.get(reverse('remesh:conversation_index'))
    self.assertEqual(response.status_code, 200)
    self.assertNotContains(response, "No conversations are available.")
    self.assertContains(response, "All Conversations")
    self.assertContains(response, "Add New Conversation")
    self.assertQuerysetEqual(response.context['conversation_list'], [conversation3, conversation, conversation2])

  def test_search_filters_to_things_that_contain_pan(self):
    conversation = create_conversation(title='Pancakes')
    conversation2 = create_conversation(title='Tacos')
    conversation3 = create_conversation(title='How many pans does it take to create 20 pancakes?')
    search_phrase = 'pan'
    response = self.client.get(reverse('remesh:conversation_index'), {'search_phrase': search_phrase})
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, f"Conversations that contain {search_phrase}")
    self.assertContains(response, "Add New Conversation")
    self.assertQuerysetEqual(response.context['conversation_list'], [conversation3, conversation])

  def test_search_filters_to_things_that_contain_words_with_space(self):
    conversation = create_conversation(title='Pancakes')
    conversation2 = create_conversation(title='Tacos')
    conversation3 = create_conversation(title='How many pans does it take to create 20 pancakes?')
    conversation4 = create_conversation(title='Taco Community')
    conversation5 = create_conversation(title='Word up to the Taco Community players')
    search_phrase = 'taco community'
    response = self.client.get(reverse('remesh:conversation_index'), {'search_phrase': search_phrase})
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, f"Conversations that contain {search_phrase}")
    self.assertContains(response, "Add New Conversation")
    self.assertQuerysetEqual(response.context['conversation_list'], [conversation4, conversation5])

  def test_search_filters_to_things_that_contain_the_number_4(self):
    conversation = create_conversation(title='Pancakes')
    conversation2 = create_conversation(title='Tacos')
    conversation3 = create_conversation(title='How many pans does it take to create 20 pancakes?')
    conversation4 = create_conversation(title='Tacos4all')
    search_phrase = '4'
    response = self.client.get(reverse('remesh:conversation_index'), {'search_phrase': search_phrase})
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, f"Conversations that contain {search_phrase}")
    self.assertContains(response, "Add New Conversation")
    self.assertQuerysetEqual(response.context['conversation_list'], [conversation4])

  def test_empty_search_phrase_shows_all_conversations(self):
    conversation = create_conversation(title='Pancakes')
    conversation2 = create_conversation(title='Tacos')
    conversation3 = create_conversation(title='How many pans does it take to create 20 pancakes?')
    search_phrase = ''
    response = self.client.get(reverse('remesh:conversation_index'), {'search_phrase': search_phrase})
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "All Conversations")
    self.assertContains(response, "Add New Conversation")
    self.assertQuerysetEqual(response.context['conversation_list'], [conversation3, conversation, conversation2])


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

  def test_add_conversation_form_post_for_valid_data_and_shows_on_index_page(self):
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
    response = self.client.get(reverse('remesh:conversation_index'))
    self.assertQuerysetEqual(response.context['conversation_list'], list(Conversation.objects.filter(title='Pancakes')))
