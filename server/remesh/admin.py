from django.contrib import admin
from .models import Conversation, Thought, Message


admin.site.register(Conversation)
admin.site.register(Thought)
admin.site.register(Message)
