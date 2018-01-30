from django.contrib import admin
from .models import *
from django.apps import apps

app = apps.get_app_config('student_portal')

# Register your models here.
admin.site.register(MessFeedback)
admin.site.register(Preference)
admin.site.register(Opi_calculated)
