from remesh.models import Team, Conversation, User
from datetime import timedelta
from django.utils import timezone


def create_user(username, password):
  user = User.objects.create_user(username=username, password=password)
  return user


def get_user_creds():
  return 'testuser', '12345'


def create_team(name, users):
  t = Team.objects.create(name=name)
  t.members.set(users)
  return t


def create_conversation(moderator, team, title='Pancakes',
                        start_date_time=timezone.now(), duration=timedelta(days=2),
                        max_num_of_participants=50
                        ):
  return Conversation.objects.create(
      title=title,
      start_date_time=start_date_time,
      duration=duration,
      max_num_of_participants=max_num_of_participants,
      moderator=moderator,
      team=team)
