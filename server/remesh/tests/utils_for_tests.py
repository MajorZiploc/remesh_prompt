from remesh.models import Conversation, Message, Thought
from datetime import timedelta
from django.utils import timezone


def create_conversation(title='Pancakes',
                        start_date_time=timezone.now()
                        ):
  return Conversation.objects.create(
      title=title,
      start_date_time=start_date_time,
  )

def create_message(conversation,
                        text='Hi there friends!',
                        date_time_sent=timezone.now()
                        ):
  return Message.objects.create(
      text=text,
      date_time_sent=date_time_sent,
      conversation=conversation
  )

def create_thought(message,
                        text='I agree with telling friends hi',
                        date_time_sent=timezone.now()
                        ):
  return Thought.objects.create(
      text=text,
      date_time_sent=date_time_sent,
      message=message
  )

