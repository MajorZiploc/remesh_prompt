# Generated by Django 3.2.3 on 2021-05-24 19:15

from django.db import migrations


class Migration(migrations.Migration):

  dependencies = [
      ('remesh', '0007_rename_conversion_conversation'),
  ]

  operations = [
      migrations.DeleteModel(
          name='Day',
      ),
      migrations.DeleteModel(
          name='WeightUnit',
      ),
  ]
