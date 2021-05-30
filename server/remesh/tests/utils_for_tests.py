from remesh.models import Conversation
from datetime import timedelta
from django.utils import timezone


def create_conversation(title='Pancakes',
                        start_date_time=timezone.now()
                        ):
  return Conversation.objects.create(
      title=title,
      start_date_time=start_date_time,
  )
