from django import forms
from .models import Report, Event, Schedule

class ReportUploadForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['event', 'summary', 'photos', 'report_pdf']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date']

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['date', 'waste_type', 'start_time', 'end_time', 'address']
        widgets = {
            'start_time': forms.TimeInput(format='%I:%M %p', attrs={'type': 'time'}),
            'end_time': forms.TimeInput(format='%I:%M %p', attrs={'type': 'time'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter collection address'}),
        }