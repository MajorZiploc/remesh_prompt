from django.contrib import admin
from .models import Team, Conversation, User, Role
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

# class DayAdmin(admin.ModelAdmin):
#   list_display = ('calories', 'morning_weight', 'body_fat_percentage', 'muscle_mass_percentage', 'day_date')


class MyUserChangeForm(UserChangeForm):
  class Meta(UserChangeForm.Meta):
    model = User


class MyUserAdmin(UserAdmin):
  form = MyUserChangeForm

  fieldsets = UserAdmin.fieldsets + (
      (None, {'fields': ('roles',)}),
  )


admin.site.register(Team)
admin.site.register(Conversation)
admin.site.register(User, MyUserAdmin)
admin.site.register(Role)
