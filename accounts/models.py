from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Custom User Table
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('admin', 'Admin'),
        ('hod', 'HOD'),   
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


# Separate Role Tables
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    email = models.EmailField()

    def __str__(self):
        return self.username


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    email = models.EmailField()

    def __str__(self):
        return self.username


class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    email = models.EmailField()

    def __str__(self):
        return self.username


# ✅ New: HOD model (optional, in case you want separate table)
class HOD(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    email = models.EmailField()

    def __str__(self):
        return self.username


# Attendance
class Attendance(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[('present', 'Present'), ('absent', 'Absent')]
    )

    def __str__(self):
        return f"{self.student.username} - {self.date} - {self.status}"


# Study Material
class StudyMaterial(models.Model):
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'}
    )
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='study_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ✅ New: Timetable model (editable only by HOD)
class TimeTable(models.Model):
    title = models.CharField(max_length=100, default="Class Timetable")
    image = models.ImageField(upload_to='timetables/',null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="timetables/")  # PDF, image, etc.
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'hod'}
    )
class DashboardBackground(models.Model):
    image = models.ImageField(upload_to='dashboard_backgrounds/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Background uploaded at {self.uploaded_at}"
    def __str__(self):
        return self.title