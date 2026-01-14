from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('hod', 'HOD'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    reg_no = models.CharField(max_length=50, blank=True, null=True)
    staff_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username
