from django.contrib import admin
from .models import User, Team  # Add others as you create

admin.site.register(User)
admin.site.register(Team)
