from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, Http404
from django.contrib import messages
from .models import Event, Volunteer, Report, Schedule
from .forms import ReportUploadForm, EventForm, ScheduleForm
import io
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import datetime
from django.contrib.admin.views.decorators import staff_member_required


def home(request):
    return render(request, 'core/home.html')


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        else:
            return redirect('resident_dashboard')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        if user.is_superuser:
            return redirect('admin_dashboard')
        else:
            return redirect('resident_dashboard')
    return render(request, 'accounts/login.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def is_admin(user):
    return user.is_superuser


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    reports = Report.objects.all().order_by('-date_uploaded')

    # Instantiate blank forms
    event_form = EventForm()
    schedule_form = ScheduleForm()

    if request.method == 'POST':
        if 'submit_event' in request.POST:
            event_form = EventForm(request.POST)
            if event_form.is_valid():
                event_form.save()
                messages.success(request, 'Event added successfully.')
                return redirect('admin_dashboard')

        elif 'submit_schedule' in request.POST:
            schedule_form = ScheduleForm(request.POST)
            if schedule_form.is_valid():
                schedule_form.save()
                messages.success(request, 'Schedule added successfully.')
                return redirect('admin_dashboard')

    context = {
        'reports': reports,
        'event_form': event_form,
        'schedule_form': schedule_form,
    }
    return render(request, 'core/admin_dashboard.html', context)

@login_required
def resident_dashboard(request):
    # Show upcoming events & weekly schedule for resident
    upcoming_events = Event.objects.filter(date__gte=datetime.date.today()).order_by('date')[:5]
    this_week_schedules = Schedule.objects.filter(
        date__gte=datetime.date.today(),
        date__lte=datetime.date.today() + datetime.timedelta(days=7)
    ).order_by('date')
    
    # Get the events that the user has joined
    joined_event_ids = Volunteer.objects.filter(user=request.user).values_list('event_id', flat=True)
    
    context = {
        'upcoming_events': upcoming_events,
        'weekly_schedules': this_week_schedules,
        'joined_event_ids': joined_event_ids,
    }
    return render(request, 'core/resident_dashboard.html', context)

@login_required
def events(request):
    events_list = Event.objects.all()

    if request.method == "POST":
        event_id = request.POST.get('event_id')
        action = request.POST.get('action', 'join')  # Default to join if not specified
        event = get_object_or_404(Event, id=event_id)

        if action == 'join':
            volunteer, created = Volunteer.objects.get_or_create(user=request.user, event=event)
            if created:
                messages.success(request, "You successfully joined the event.")
            else:
                messages.info(request, "You already joined this event.")
        elif action == 'unjoin':
            try:
                volunteer = Volunteer.objects.get(user=request.user, event=event)
                volunteer.delete()
                messages.success(request, "You have successfully unjoined from the event.")
            except Volunteer.DoesNotExist:
                messages.error(request, "You were not joined to this event.")
        
        return redirect('events')
    
    joined_event_ids = Volunteer.objects.filter(user=request.user).values_list('event_id', flat=True)

    return render(request, 'core/events.html', {
        'events': events_list,
        'joined_event_ids': joined_event_ids,
    })


@login_required
def schedules(request):
    schedules = Schedule.objects.all().order_by('date')
    return render(request, 'core/schedules.html', {'schedules': schedules})


@login_required
def upload_report(request):
    if request.method == 'POST':
        form = ReportUploadForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            messages.success(request, "Report uploaded successfully.")
            return redirect('resident_dashboard')
    else:
        form = ReportUploadForm()
    return render(request, 'core/upload_report.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def volunteers(request):
    volunteers = Volunteer.objects.select_related('user', 'event').all()
    return render(request, 'core/volunteers.html', {'volunteers': volunteers})


@login_required
@user_passes_test(is_admin)
def report_pdf(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    template_path = 'core/report_pdf.html'
    context = {'report': report}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{report.id}.pdf"'

    html = render_to_string(template_path, context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@staff_member_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events')  # replace with your events list view name
    else:
        form = EventForm(instance=event)
    return render(request, 'core/edit_event.html', {'form': form})

@staff_member_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('events')  # replace with your events list view name