# Generated by Django 3.2.3 on 2021-05-30 19:28

from django.db import migrations


class Migration(migrations.Migration):

  dependencies = [
      ('remesh', '0002_auto_20210530_1053'),
  ]

  operations = [
      migrations.AlterModelOptions(
          name='conversation',
          options={'ordering': ['start_date_time', 'title']},
      ),
      migrations.AlterModelOptions(
          name='message',
          options={'ordering': ['date_time_sent', 'text']},
      ),
      migrations.AlterModelOptions(
          name='thought',
          options={'ordering': ['date_time_sent', 'text']},
      ),
  ]
