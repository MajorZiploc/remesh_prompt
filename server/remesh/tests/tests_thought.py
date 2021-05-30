from django.test import TestCase
from django.urls import reverse
from remesh.models import Thought
from .utils_for_tests import *
from django.utils import timezone
from datetime import timedelta


class ThoughtIndexViewTests(TestCase):
  def test_no_thoughts(self):
    conversation = create_conversation(title='Tacos')
    message = create_message(text='No thank you to the tacos', conversation=conversation)
    response = self.client.get(reverse('remesh:thought_index', args=(message.pk,)))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No thoughts are available.")
    self.assertContains(response, "Add New Thought")
    self.assertQuerysetEqual(response.context['thought_list'], [])

  def test_thought_is_in_index_with_thought_text(self):
    conversation = create_conversation(title='Tacos')
    message = create_message(text='No thank you to the tacos', conversation=conversation)
    thought = create_thought(text='You dont want tacos!?', message=message)
    thought2 = create_thought(text='I love tacos so much!', message=message)
    response = self.client.get(reverse('remesh:thought_index', args=(message.pk,)))
    self.assertEqual(response.status_code, 200)
    self.assertNotContains(response, "No thoughts are available.")
    self.assertContains(response, "Thoughts")
    self.assertContains(response, "Add New Thought")
    self.assertContains(response, "You dont want tacos!?")
    self.assertContains(response, "I love tacos so much!")
    self.assertQuerysetEqual(response.context['thought_list'], [thought2, thought])


class ThoughtAddFormTests(TestCase):
  def test_add_thought_form_exists(self):
    conversation = create_conversation(title='Tacos')
    message = create_message(text='No thank you to the tacos', conversation=conversation)
    response = self.client.get(reverse('remesh:thought_add', args=(message.pk,)))
    self.assertEqual(response.status_code, 200)
    labels = [
        'Text',
        'Date time sent',
        'Submit']
    for label in labels:
      self.assertContains(response, label)

  def test_add_thought_form_post_for_valid_data(self):
    conversation = create_conversation(title='Tacos')
    message = create_message(text='No thank you to the tacos', conversation=conversation)
    response = self.client.post(
      reverse('remesh:thought_add', args=(message.pk,)),
      data={
        'text': 'I love tacos!',
        'date_time_sent': "01/01/2020",
        'message': message.pk
      }
    )
    self.assertRedirects(response, reverse('remesh:thought_index', args=(message.pk,)))
    c = Thought.objects.all().count()
    self.assertEqual(c, 1)

  def test_added_thoughts_show_under_right_message(self):
    conversation = create_conversation(title='Tacos')
    message = create_message(text='No thank you to the tacos', conversation=conversation)
    message1 = create_message(text='I love tacos!?', conversation=conversation)
    response1 = self.client.post(
      reverse('remesh:thought_add', args=(message1.pk,)),
      data={
        'text': 'I love them too!',
        'date_time_sent': "01/01/2020",
        'message': message.pk
      }
    )
    response = self.client.post(
      reverse('remesh:thought_add', args=(message.pk,)),
      data={
        'text': 'How could you not love tacos??',
        'date_time_sent': "01/01/2020",
        'message': message.pk
      }
    )
    self.assertRedirects(response, reverse('remesh:thought_index', args=(message.pk,)))
    response = self.client.get(reverse('remesh:thought_index', args=(message.pk,)))
    self.assertQuerysetEqual(
        response.context['thought_list'], list(
            Thought.objects.filter(
                text='How could you not love tacos??')))
