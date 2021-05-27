from django.contrib import admin
from .models import Team, Conversation
from django.contrib.auth.admin import UserAdmin
from .models import User

# class DayAdmin(admin.ModelAdmin):
#   list_display = ('calories', 'morning_weight', 'body_fat_percentage', 'muscle_mass_percentage', 'day_date')

admin.site.register(Team)
admin.site.register(Conversation)
admin.site.register(User, UserAdmin)
