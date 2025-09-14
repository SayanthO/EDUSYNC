from django.urls import path
from . import views

urlpatterns = [
    # Home & Auth
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
   
    # Dashboards
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('parent/dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('hod/dashboard/', views.hod_dashboard, name='hod_dashboard'),

    # Attendance
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/view/', views.view_attendance, name='view_attendance'),
    path('attendance/report/', views.attendance_report, name='attendance_report'),

    # Study Materials
    path('materials/upload/', views.upload_study_material, name='upload_study_material'),
    path('materials/view/', views.view_study_materials, name='view_study_materials'),

    # Timetable
    path('timetable/edit/', views.edit_timetable, name='edit_timetable'),
]
