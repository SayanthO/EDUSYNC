import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()  # Custom user if defined

# ---------------- HOME & AUTH ----------------

def home(request):
    return render(request, 'accounts/home.html')


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email", "").strip()
        role = request.POST.get("role")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("signup")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.role = role
        user.save()

       # ...existing code...
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Role-based redirection
            role = getattr(user, 'role', None)
            if role == 'student':
                return redirect('student_dashboard')
            elif role == 'teacher':
                return redirect('teacher_dashboard')
            elif role == 'hod':
                return redirect('hod_dashboard')
            elif role == 'parent':
                return redirect('parent_dashboard')
            else:
                return redirect('home')
        else:
            messages.success(request, "Account created successfully!")
            return redirect("login")
# ...existing code...

    return render(request, "accounts/signup.html")


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Role-based redirection
            role = getattr(user, 'role', None)
            if role == 'student':
                return redirect('student_dashboard')
            elif role == 'teacher':
                return redirect('teacher_dashboard')
            elif role == 'hod':
                return redirect('hod_dashboard')
            elif role == 'parent':
                return redirect('parent_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


# ---------------- DASHBOARDS ----------------

@login_required
def student_dashboard(request):
    return render(request, 'accounts/student_dashboard.html')


@login_required
def teacher_dashboard(request):
    return render(request, 'accounts/teacher_dashboard.html')


@login_required
def parent_dashboard(request):
    return render(request, 'accounts/parent_dashboard.html')


@login_required
def hod_dashboard(request):
    return render(request, 'accounts/hod_dashboard.html')


# ---------------- ATTENDANCE ----------------

@login_required
def mark_attendance(request):
    return render(request, 'accounts/mark_attendance.html')


@login_required
def view_attendance(request):
    return render(request, 'accounts/view_attendance.html')


@login_required
def attendance_report(request):
    return render(request, 'accounts/attendance_report.html')


# ---------------- STUDY MATERIALS ----------------

@login_required
def upload_study_material(request):
    return render(request, 'accounts/upload_study_material.html')


@login_required
def view_study_materials(request):
    return render(request, 'accounts/view_study_materials.html')


# ---------------- TIMETABLE ----------------

@login_required
def edit_timetable(request):
    if getattr(request.user, "role", None) != 'hod':
        messages.error(request, "You are not authorized to access this page.")
        return redirect('home')

    save_dir = os.path.join(settings.MEDIA_ROOT, 'timetables')
    os.makedirs(save_dir, exist_ok=True)
    fs = FileSystemStorage(location=save_dir)

    timetable_url = None
    if os.path.exists(os.path.join(save_dir, 'timetable.png')):
        timetable_url = settings.MEDIA_URL + 'timetables/timetable.png'

    if request.method == 'POST' and request.FILES.get('timetable'):
        timetable_file = request.FILES['timetable']
        fs.save('timetable.png', timetable_file)
        messages.success(request, "✅ Timetable updated successfully!")
        return redirect('hod_dashboard')

    return render(request, 'accounts/edit_timetable.html', {'timetable_url': timetable_url})
