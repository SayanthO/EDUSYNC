from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_page, name='welcome'),
    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('signup/role/', views.signup_role, name='signup_role'),
    path('signup/student/', views.signup_student, name='signup_student'),
    path('signup/teacher/', views.signup_teacher, name='signup_teacher'),
    path('signup/hod/', views.signup_hod, name='signup_hod'),

    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/hod/', views.hod_dashboard, name='hod_dashboard'),
]
