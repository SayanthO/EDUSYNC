# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

# Choices for user role and classes
ROLE_CHOICES = (
    ('student', 'Student'),
    ('teacher', 'Teacher'),
    ('hod', 'HOD'),
)

CLASS_CHOICES = [
    ('CPS1', 'CPS1'),
    ('CPS2', 'CPS2'),
    ('CPS3', 'CPS3'),
    ('CPS4', 'CPS4'),
    ('CPS5', 'CPS5'),
    ('CPS6', 'CPS6'),
]

DAYS_OF_WEEK = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    reg_no = models.CharField(max_length=20, unique=True, null=True, blank=True)
    staff_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    student_class = models.CharField(max_length=10, choices=CLASS_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.username

# HOD Timetable model for each class
class ClassTimetable(models.Model):
    class_name = models.CharField(max_length=10, choices=CLASS_CHOICES)
    day = models.CharField(max_length=10, choices=[(d, d) for d in DAYS_OF_WEEK])
    period1 = models.CharField(max_length=50, blank=True)
    period2 = models.CharField(max_length=50, blank=True)
    period3 = models.CharField(max_length=50, blank=True)
    period4 = models.CharField(max_length=50, blank=True)
    period5 = models.CharField(max_length=50, blank=True)
    period6 = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.class_name} - {self.day}"
