from django.contrib import admin
from .models import Team, Conversation


# class DayAdmin(admin.ModelAdmin):
#   list_display = ('calories', 'morning_weight', 'body_fat_percentage', 'muscle_mass_percentage', 'day_date')

admin.site.register(Team)
admin.site.register(Conversation)
