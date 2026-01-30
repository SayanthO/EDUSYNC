# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, ClassTimetable

# --- Welcome page ---
def welcome_page(request):
    return render(request, 'accounts/welcome.html')


# --- Login view ---
def login_view(request):
    if request.method == "POST":
        reg_no = request.POST.get("registernumber")
        password = request.POST.get("password")

        user = authenticate(request, username=reg_no, password=password)

        if user is not None:
            login(request, user)
            # Role-based redirect
            if user.role == "student":
                return redirect("student_dashboard")
            elif user.role == "teacher":
                return redirect("teacher_dashboard")
            elif user.role == "hod":
                return redirect("hod_dashboard")
            else:
                messages.error(request, "Role not assigned")
        else:
            messages.error(request, "Invalid Register Number or Password")

    return render(request, "accounts/login.html")


# --- Logout ---
def logout_view(request):
    logout(request)
    return redirect('login')


# --- Signup pages ---
def signup_role(request):
    return render(request, 'accounts/signup_role.html')


# --- Student signup ---
def signup_student(request):
    from .models import CustomUser
    if request.method == "POST":
        full_name = request.POST['full_name']
        reg_no = request.POST['reg_no']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']
        student_class = request.POST.get('student_class')  # Class selection

        if password != confirm:
            messages.error(request, "Passwords do not match!")
            return redirect('signup_student')

        if CustomUser.objects.filter(username=reg_no).exists():
            messages.error(request, "Register number already exists!")
            return redirect('signup_student')

        user = CustomUser.objects.create_user(
            username=reg_no,
            first_name=full_name,
            email=email,
            password=password,
            role='student',
            reg_no=reg_no,
            student_class=student_class
        )
        login(request, user)
        return redirect('student_dashboard')

    return render(request, 'accounts/signup_student.html')


# --- Teacher signup ---
def signup_teacher(request):
    if request.method == "POST":
        full_name = request.POST['full_name']
        staff_id = request.POST['staff_id']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password != confirm:
            messages.error(request, "Passwords do not match!")
            return redirect('signup_teacher')

        if CustomUser.objects.filter(username=staff_id).exists():
            messages.error(request, "Staff ID already exists!")
            return redirect('signup_teacher')

        user = CustomUser.objects.create_user(
            username=staff_id,
            first_name=full_name,
            email=email,
            password=password,
            role='teacher',
            staff_id=staff_id
        )
        messages.success(request, "Teacher account created!")
        return redirect('login')

    return render(request, 'accounts/signup_teacher.html')


# --- HOD signup ---
def signup_hod(request):
    if request.method == "POST":
        full_name = request.POST['full_name']
        hod_id = request.POST['hod_id']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password != confirm:
            messages.error(request, "Passwords do not match!")
            return redirect('signup_hod')

        if CustomUser.objects.filter(username=hod_id).exists():
            messages.error(request, "HOD ID already exists!")
            return redirect('signup_hod')

        user = CustomUser.objects.create_user(
            username=hod_id,
            first_name=full_name,
            email=email,
            password=password,
            role='hod',
            staff_id=hod_id
        )
        messages.success(request, "HOD account created!")
        return redirect('login')

    return render(request, 'accounts/signup_hod.html')


# --- Dashboards ---
@login_required(login_url="login")
def student_dashboard(request):
    from .models import ClassTimetable
    timetable = None
    if request.user.student_class:
        timetable = ClassTimetable.objects.filter(class_name=request.user.student_class)
    context = {
        "timetable": timetable
    }
    return render(request, "accounts/student_dashboard.html", context)


@login_required(login_url="login")
def teacher_dashboard(request):
    return render(request, "accounts/teacher_dashboard.html")


@login_required(login_url="login")
def hod_dashboard(request):
    from .models import ClassTimetable
    timetable = ClassTimetable.objects.all()
    context = {
        "timetable": timetable
    }
    return render(request, 'accounts/hod_dashboard.html', context)
