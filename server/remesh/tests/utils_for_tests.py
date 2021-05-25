from remesh.models import Team, Conversation
from django.contrib.auth.models import User
from datetime import datetime, timedelta

def create_user(username, password):
  user = User.objects.create_user(username=username, password=password)
  return user


def get_user_creds():
  return 'testuser', '12345'


def create_team(users):
  t = Team.objects.create()
  t.members.set(users)
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

