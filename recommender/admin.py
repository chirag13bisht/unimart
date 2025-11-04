from django.contrib import admin
from .models import UserEvent

# This line tells the admin to show the UserEvent model
admin.site.register(UserEvent)