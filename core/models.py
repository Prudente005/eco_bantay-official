from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Schedule(models.Model):
    date = models.DateField()
    waste_type = models.CharField(max_length=100)
    start_time = models.TimeField(default="08:00:00")
    end_time = models.TimeField()
    address = models.CharField(max_length=200, default="")

    def __str__(self):
        return f"{self.date} - {self.waste_type}"

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    summary = models.TextField()
    photos = models.ImageField(upload_to='report_photos/', blank=True, null=True)
    report_pdf = models.FileField(upload_to='report_pdfs/', blank=True, null=True)

    def __str__(self):
        return f"Report by {self.user.username} for {self.event.title}"

class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    joined_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} volunteering for {self.event.title}"
