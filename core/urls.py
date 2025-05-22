from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('resident-dashboard/', views.resident_dashboard, name='resident_dashboard'),

    path('events/', views.events, name='events'),
    path('schedules/', views.schedules, name='schedules'),
    path('upload-report/', views.upload_report, name='upload_report'),
    path('volunteers/', views.volunteers, name='volunteers'),

    path('report-pdf/<int:report_id>/', views.report_pdf, name='report_pdf'),
    path('event/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('event/delete/<int:event_id>/', views.delete_event, name='delete_event'),
]
