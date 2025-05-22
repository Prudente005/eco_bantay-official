from django.contrib import admin
from .models import Event, Schedule, Volunteer, Report

admin.site.register(Event)
admin.site.register(Schedule)
admin.site.register(Volunteer)
admin.site.register(Report)
