from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class WeightUnit(models.Model):
  name = models.CharField(max_length=250)
  label = models.CharField(max_length=100)

  def __str__(self):
    return self.name


class Day(models.Model):
  fit_user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE
    )
  weight_units = models.ForeignKey(WeightUnit, on_delete=models.CASCADE)
  calories = models.IntegerField(default=0)
  morning_weight = models.FloatField(default=0.0)
  body_fat_percentage = models.FloatField(default=0.0)
  muscle_mass_percentage = models.FloatField(default=0.0)
  day_date = models.DateField()

  def __str__(self):
    return f'{self.day_date} {self.calories}'


class Team(models.Model):
  members = models.ManyToManyField(User)


class Conversation(models.Model):
  title = models.CharField(max_length=250)
  date = models.DateField()
  start_time = models.TimeField(auto_now=False, auto_now_add=False)
  duration = models.DurationField()
  max_num_of_participants = models.PositiveIntegerField()
  moderator = models.ForeignKey(User, on_delete=models.CASCADE)
  team = models.ForeignKey(Team, on_delete=models.CASCADE)
