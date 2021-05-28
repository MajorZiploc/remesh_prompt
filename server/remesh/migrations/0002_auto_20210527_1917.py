# Generated by Django 3.2.3 on 2021-05-28 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remesh', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.PositiveSmallIntegerField(choices=[(1, 'participant'), (2, 'teammember'), (3, 'chatmoderator'), (4, 'admin')], primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(to='remesh.Role'),
        ),
    ]