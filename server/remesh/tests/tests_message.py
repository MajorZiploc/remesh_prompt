from django.test import TestCase
from django.urls import reverse
from remesh.models import Message
from .utils_for_tests import *
from django.utils import timezone
from datetime import timedelta


class MessageIndexViewTests(TestCase):
  def test_no_messages_empty_index(self):
    conversation = create_conversation(title='Tacos')
    response = self.client.get(reverse('remesh:message_index', args=(conversation.pk,)))
    self.assertEqual(response.status_code, 200)
    self.assertNotContains(response, "All Messages")
    self.assertNotContains(response, "Messages that contain")
    self.assertContains(response, "No messages are available.")
    self.assertContains(response, "Add New Message")
    self.assertQuerysetEqual(response.context['message_list'], [])

  def test_message_is_in_index_with_message_text_for_a_given_conversation_in_order(self):
    conversation = create_conversation(title='Party Tacos')
    conversation2 = create_conversation(title='Pancakes')
    message = create_message(
        text='No thank you to the tacos',
        conversation=conversation,
        date_time_sent=(
            timezone.now() -
            timedelta(
                days=1)))
    message2 = create_message(text='I love tacos so much!', conversation=conversation)
    message3 = create_message(text='I love pancakes so much!', conversation=conversation2)
    response = self.client.get(reverse('remesh:message_index', args=(conversation.pk,)))
    self.assertEqual(response.status_code, 200)
    self.assertNotContains(response, "No messages are available.")
    self.assertContains(response, "All Messages")
    self.assertContains(response, "Party Tacos")
    self.assertContains(response, "Add New Message")
    self.assertContains(response, "I love tacos so much!")
    self.assertContains(response, "No thank you to the tacos")
    self.assertQuerysetEqual(response.context['message_list'], [message, message2])

  def test_search_filters_to_things_that_contain_words_with_space(self):
    conversation = create_conversation(title='Tacos')
    message = create_message(text='No thank you 4 the taco Community', conversation=conversation)
    message2 = create_message(text='I love tacos so much!', conversation=conversation)
    message3 = create_message(text='Ok but srsly? taco LOVE', conversation=conversation)
    search_phrase = 'taco community'
    response = self.client.get(
        reverse(
            'remesh:message_index', args=(
                conversation.pk,)), {
            'search_phrase': search_phrase})
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, f"Messages that contain {search_phrase}")
    self.assertContains(response, "Add New Message")
    self.assertQuerysetEqual(response.context['message_list'], [message])

  def test_search_filters_to_things_that_contain_the_number_4(self):
    conversation = create_conversation(title='Tacos')
    message = create_message(text='No thank you 4 the tacos', conversation=conversation)
    message2 = create_message(text='I love tacos so much!', conversation=conversation)
    message3 = create_message(text='Ok but srsly? taco LOVE', conversation=conversation)
    search_phrase = '4'
    response = self.client.get(
        reverse(
            'remesh:message_index', args=(
                conversation.pk,)), {
            'search_phrase': search_phrase})
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, f"Messages that contain {search_phrase}")
    self.assertContains(response, "Add New Message")
    self.assertQuerysetEqual(response.context['message_list'], [message])

  def test_search_filters_to_things_that_contain_love(self):
    conversation = create_conversation(title='Tacos')
    message = create_message(text='No thank you to the tacos', conversation=conversation)
    message2 = create_message(text='I love tacos so much!', conversation=conversation)
    message3 = create_message(text='Ok but srsly? taco LOVE', conversation=conversation)
    search_phrase = 'love'
    response = self.client.get(
        reverse(
            'remesh:message_index', args=(
                conversation.pk,)), {
            'search_phrase': search_phrase})
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, f"Messages that contain {search_phrase}")
    self.assertContains(response, "Add New Message")
    self.assertQuerysetEqual(response.context['message_list'], [message2, message3])

  def test_empty_search_phrase_shows_all_messages_for_a_given_conversation(self):
    conversation = create_conversation(title='Tacos')
    conversation2 = create_conversation(title='Pancakes')
    message = create_message(text='No thank you to the tacos', conversation=conversation)
    message2 = create_message(text='I love tacos so much!', conversation=conversation)
    message3 = create_message(text='Ok but srsly? taco LOVE', conversation=conversation)
    message4 = create_message(text='Pancake life', conversation=conversation2)
    search_phrase = ''
    response = self.client.get(
        reverse(
            'remesh:message_index', args=(
                conversation.pk,)), {
            'search_phrase': search_phrase})
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "All Messages")
    self.assertContains(response, "Add New Message")
    self.assertQuerysetEqual(response.context['message_list'], [message2, message, message3])


class MessageAddFormTests(TestCase):
  def test_add_message_form_exists(self):
    conversation = create_conversation(title='Tacos')
    response = self.client.get(reverse('remesh:message_add', args=(conversation.pk,)))
    self.assertEqual(response.status_code, 200)
    labels = [
        'Text',
        'Date time sent',
        'Submit']
    for label in labels:
      self.assertContains(response, label)

  def test_add_message_form_post_for_valid_data(self):
    conversation = create_conversation(title='Tacos')
    response = self.client.post(
      reverse('remesh:message_add', args=(conversation.pk,)),
      data={
        'text': 'I love tacos!',
        'date_time_sent': "01/01/2020",
        'conversation': conversation.pk
      }
    )
    self.assertRedirects(response, reverse('remesh:message_index', args=(conversation.pk,)))
    c = Message.objects.all().count()
    self.assertEqual(c, 1)

  def test_added_messages_show_under_right_conversation(self):
    conversation = create_conversation(title='Tacos')
    conversation1 = create_conversation(title='Not Tacos')
    response1 = self.client.post(
      reverse('remesh:message_add', args=(conversation1.pk,)),
      data={
        'text': 'not a taco chat',
        'date_time_sent': "01/01/2020",
        'conversation': conversation.pk
      }
    )
    response = self.client.post(
      reverse('remesh:message_add', args=(conversation.pk,)),
      data={
        'text': 'I love tacos!',
        'date_time_sent': "01/01/2020",
        'conversation': conversation.pk
      }
    )
    self.assertRedirects(response, reverse('remesh:message_index', args=(conversation.pk,)))
    response = self.client.get(reverse('remesh:message_index', args=(conversation.pk,)))
    self.assertQuerysetEqual(response.context['message_list'], list(Message.objects.filter(text='I love tacos!')))
