from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Course, Alumni, Student, Events, AlumniJob
import datetime

def home(request):
    return render(request, 'index.html')

def user_logout(request):
    logout(request)  # Django's built-in logout function
    return redirect('home')

def admin_dashboard(request):
    if request.user.is_superuser:
        return render(request, 'admin_index.html')
    else:
        return redirect('home')
    
def admin_course(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        title = request.POST.get('title')
        course_id = request.POST.get('course_id')

        if action == 'add':
            if title:
                Course.objects.create(title=title)
                print("Course added successfully.")
            else:
                print("Course title is required.")
        
        elif action == 'delete':
            if course_id:
                Course.objects.filter(id=course_id).delete()
                print("Course deleted successfully.")
            else:
                print("Course ID is required.")

        return redirect('admin_course')  # Redirect to the same page after processing

    courses = Course.objects.all()  # Fetch all courses
    return render(request, 'admin_course.html', {'courses': courses})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Fetch the user using the email
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Pass an error message if the email does not exist
            return render(request, 'login.html', {'error': "User with this email does not exist."})

        # Check if the password matches
        if user.check_password(password):
            # Log the user in
            login(request, user)

            # Check if the user is a superuser
            if user.is_superuser:
                return redirect('admin_dashboard')

            # Check if the user is a student
            try:
                student = Student.objects.get(email=user.email)
                if not student.is_approved:
                    # Display an error message if the student account is not approved
                    return render(request, 'login.html', {'error': "Your student account is not approved yet. Please contact the administrator."})
                return redirect('student_index')
            except Student.DoesNotExist:
                # Check if the user is an alumni
                try:
                    alumni = Alumni.objects.get(email=user.email)
                    if not alumni.is_approved:
                        # Display an error message if the alumni account is not approved
                        return render(request, 'login.html', {'error': "Your alumni account is not approved yet. Please contact the administrator."})
                    return redirect('alumni_index')
                except Alumni.DoesNotExist:
                    # Display an error message if the user is not a student or alumni
                    return render(request, 'login.html', {'error': "Your account does not belong to a student or alumni."})
        else:
            # Display an error message if the password is incorrect
            return render(request, 'login.html', {'error': "Invalid email or password."})

    return render(request, 'login.html')

def register_student(request):
    error = None
    if request.method == 'POST':
        # Get form data
        adnum = request.POST.get('adnum')
        course_id = request.POST.get('course')
        name = request.POST.get('name')
        number = request.POST.get('number')
        email = request.POST.get('email')
        password = request.POST.get('password')  # Consider hashing in production
        image = request.FILES.get('image')  # Handle file upload
        
        # Check if email is already registered
        if Student.objects.filter(email=email).exists():
            error = "Email is already registered."
        elif len(number) != 10:
            error = "Phone number must be exactly 10 digits."
        else:
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                error = "Selected course does not exist."
            else:
                User = get_user_model()
                user = User.objects.create_user(username=name, email=email, password=password)

                # Create a new Student instance and save it
                student = Student(
                    adnum=adnum,
                    course=course,
                    name=name,
                    number=number,
                    email=email,
                    password=password,  # Again, consider hashing
                    image=image
                )
                student.save()

                return redirect('login')  # Redirect to login or another page
    
    courses = Course.objects.all()

    return render(request, 'register_student.html', {'courses': courses, 'error': error})

def register_alumini(request):
    error_message = None  # Initialize error message variable

    if request.method == 'POST':
        name = request.POST.get('name')
        course_id = request.POST.get('course')  # Get the selected course ID
        passout = request.POST.get('passout')
        number = request.POST.get('number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('image')  # Handling file upload

        # Validate phone number length
        if len(number) != 10:
            error_message = "Phone number must be exactly 10 digits."
            return render(request, 'register_alumini.html', {'error': error_message, 'courses': Course.objects.all(), 'current_year': datetime.datetime.now().year})

        # Validate year of passout
        current_year = datetime.datetime.now().year
        if int(passout) < current_year - 50 or int(passout) > current_year:
            error_message = "Year of passout must be between the last 50 years and the current year."
            return render(request, 'register_alumini.html', {'error': error_message, 'courses': Course.objects.all(), 'current_year': current_year})

        # Ensure course ID is valid
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            error_message = "Selected course does not exist."
            return render(request, 'register_alumini.html', {'error': error_message, 'courses': Course.objects.all(), 'current_year': current_year})

        # Check if email is already registered
        if Alumni.objects.filter(email=email).exists():
            error_message = "Email already registered."
            return render(request, 'register_alumini.html', {'error': error_message, 'courses': Course.objects.all(), 'current_year': current_year})
        
        User = get_user_model()
        user = User.objects.create_user(username=name, email=email, password=password)

        # Create the Alumni instance and save it
        alumni = Alumni(
            name=name,
            course=course,  # Ensure this is a valid Course object
            passout=passout,
            number=number,
            email=email,
            password=password,  # Consider hashing this password in a real application
            image=image
        )
        alumni.save()

        return redirect('login')  # Redirect to a success page or home page
    
    courses = Course.objects.all()
    current_year = datetime.datetime.now().year

    return render(request, 'register_alumini.html', {'courses': courses, 'current_year': current_year})

def users_list(request):
    students = Student.objects.filter(is_approved=True)
    alumni = Alumni.objects.filter(is_approved=True)
    return render(request, 'users_list.html', {'students': students, 'alumni': alumni})

def delete_user(request, email):
    # Try to delete the user from Student model
    try:
        student = Student.objects.get(email=email)
        student.delete()
        print('Student deleted successfully.')
    except Student.DoesNotExist:
        # If not found in Student model, check Alumni model
        try:
            alumni = Alumni.objects.get(email=email)
            alumni.delete()
            print('Alumni deleted successfully.')
        except Alumni.DoesNotExist:
            print('User not found.')
    
    return redirect('users_list')
    
def user_request(request):
    student_requests = Student.objects.filter(is_approved=False)
    alumni_requests = Alumni.objects.filter(is_approved=False)
    
    return render(request, 'user_request.html', {
        'student_requests': student_requests,
        'alumni_requests': alumni_requests,
    })

def approve_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.is_approved = True
    student.save()
    return redirect('user_request')

def approve_alumni(request, alumni_id):
    alumni = get_object_or_404(Alumni, id=alumni_id)
    alumni.is_approved = True
    alumni.save()
    return redirect('user_request')

def reject_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student_name = student.name  # Store the name for debugging
    student.delete()  # Delete the student record from the database
    print(f"Student {student_name} has been deleted.")  # Debugging output
    return redirect('user_request')  # Redirect to the user_request page

def reject_alumni(request, alumni_id):
    alumni = get_object_or_404(Alumni, id=alumni_id)
    alumni_name = alumni.name  # Store the name for debugging
    alumni.delete()  # Delete the alumni record from the database
    print(f"Alumni {alumni_name} has been deleted.")  # Debugging output
    return redirect('user_request')  # Redirect to the user_request page



def student_index(request):
    return render(request, 'student_index.html')

def alumni_index(request):
    return render(request, 'alumni_index.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        number = request.POST.get('phone_number')

        try:
            # Check if the user exists in the Student table
            student = Student.objects.get(email=email, number=number)
            print(f'Student found: {student}')
            return redirect('change_password', user_id=student.id)  # Pass the student ID

        except Student.DoesNotExist:
            try:
                # If not in Student, check if the user exists in the Alumni table
                alumni = Alumni.objects.get(email=email, number=number)
                print(f'Alumni found: {alumni}')
                return redirect('change_password', user_id=alumni.id)  # Pass the alumni ID

            except Alumni.DoesNotExist:
                # If not found in either table, show an error message
                return render(request, 'forgot_password.html', {'error': 'No matching user found.'})

    return render(request, 'forgot_password.html')

def change_password(request, user_id):
    try:
        # Try to fetch the user from the Student table
        user = None
        student = Student.objects.filter(id=user_id).first()
        if student:
            user = student
            print(f'student got: {student}')
        else:
            # Try to fetch the user from the Alumni table
            alumni = Alumni.objects.filter(id=user_id).first()
            if alumni:
                user = alumni
                print(f'alumni got: {alumni}')
            else:
                return render(request, 'change_password.html', {'error': 'User does not exist.'})

    except Exception as e:
        print(e)  # Log the exception for debugging
        return render(request, 'change_password.html', {'error': 'An error occurred.'})

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password and confirm_password:
            if new_password == confirm_password:
                # Hash the password using make_password and save to the auth_user model
                hashed_password = make_password(new_password)
                auth_user = get_user_model()

                # Find the corresponding user in the auth_user table using email
                auth_user_instance = auth_user.objects.get(email=user.email)
                auth_user_instance.password = hashed_password
                auth_user_instance.save()

                # Update the Student or Alumni model
                user.password = hashed_password
                user.save()

                print("Password updated successfully")
                return redirect('login')  # Redirect to login or another success page
            else:
                return render(request, 'change_password.html', {'error': 'Passwords do not match.'})

    return render(request, 'change_password.html', {'user_id': user_id})

def admin_events(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        event_id = request.POST.get('event_id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        venue = request.POST.get('venue')

        if action == 'add':
            if title and description and date and venue:
                Events.objects.create(name=title, description=description, date=date, venue=venue)
                print("Event added successfully.")
            else:
                print("All fields are required.")

        elif action == 'delete':
            if event_id:
                Events.objects.filter(id=event_id).delete()
                print("Event deleted successfully.")
            else:
                print("Event ID is required.")

        return redirect('admin_events')

    events = Events.objects.all()
    return render(request, 'admin_events.html', {'events': events})

def student_events(request):
    events = Events.objects.all()
    return render(request, 'student_events.html', {'events': events})

def view_alumnies(request):
    # Fetch all approved alumni
    alumnies = Alumni.objects.filter(is_approved=True)
    context = {
        'alumnies': alumnies,
    }
    
    return render(request, 'view_alumnies.html', context)

def student_profile(request):
    student = get_object_or_404(Student, email=request.user.email)  # assuming email is unique
    courses = Course.objects.all()

    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.course_id = request.POST.get('course')
        student.passout = request.POST.get('passout')
        student.number = request.POST.get('number')

        if 'image' in request.FILES:
            student.image = request.FILES['image']

        student.is_approved=False
        student.save()
        return redirect('student_profile')
    return render(request, 'student_profile.html', {'courses': courses, 'student': student})

def alumni_events(request):
    events = Events.objects.all()
    return render(request, 'alumni_events.html', {'events': events})

def alumni_profile(request):
    alumni = get_object_or_404(Alumni, email=request.user.email)  # assuming email is unique
    courses = Course.objects.all()

    if request.method == 'POST':
        alumni.name = request.POST.get('name')
        alumni.course_id = request.POST.get('course')
        alumni.passout = request.POST.get('passout')
        alumni.number = request.POST.get('number')

        if 'image' in request.FILES:
            alumni.image = request.FILES['image']

        alumni.is_approved=False
        alumni.save()
        return redirect('alumni_profile')
    return render(request, 'alumni_profile.html', {'courses': courses, 'alumni': alumni})

def alumni_job_status(request):
    alumni = get_object_or_404(Alumni, email=request.user.email)
    jobs = AlumniJob.objects.filter(alumni=alumni)
    return render(request, 'alumni_job_status.html', {'jobs': jobs})

@login_required
def alumni_post_job(request):
    # Fetch the current logged-in user
    current_user = request.user

    # Fetch alumni instance for the current user
    try:
        alumni = Alumni.objects.get(email=current_user.email)  # Assuming email links user to alumni
    except Alumni.DoesNotExist:
        alumni = None

    if request.method == 'POST':
        if alumni is not None:  # Ensure alumni instance is valid
            action = request.POST.get('action')

            if action == 'add':
                company_name = request.POST.get('company_name')
                role = request.POST.get('role')
                date_joined = request.POST.get('date_joined')
                salary = request.POST.get('salary')
                # Assuming you have an image upload
                image = request.FILES.get('image')  # Accessing the uploaded image

                # Create a new job posting
                new_job = AlumniJob(
                    alumni=alumni,  # Use the alumni instance
                    company_name=company_name,
                    role=role,
                    date_joined=date_joined,
                    salary=salary,
                    image=image  # Ensure image is included
                )
                new_job.save()  # Save the new job instance
                return redirect('alumni_post_job')  # Redirect after posting

            elif action == 'delete':
                job_id = request.POST.get('job_id')
                try:
                    job_to_delete = AlumniJob.objects.get(id=job_id, alumni=alumni)
                    job_to_delete.delete()  # Delete the job if found
                except AlumniJob.DoesNotExist:
                    pass  # Handle if job does not exist

    # Fetch all jobs posted by the current alumni
    jobs = AlumniJob.objects.filter(alumni=alumni) if alumni else []

    return render(request, 'alumni_post_job.html', {'jobs': jobs})

@login_required
def admin_job_post(request):
    job_requests = AlumniJob.objects.filter(approved=False)
    jobs = AlumniJob.objects.filter(approved=True)
    return render(request, 'admin_job_post.html', {'job_requests': job_requests, 
                                                   'jobs': jobs})

@login_required
def approve_job(request, job_id):
    # Approve a specific job request
    job_request = get_object_or_404(AlumniJob, id=job_id)
    job_request.approved = True  # Set approved status
    job_request.save()  # Save changes
    return redirect('admin_job_post')  # Redirect back to the job requests page

@login_required
def reject_job(request, job_id):
    # Reject a specific job request
    job_request = get_object_or_404(AlumniJob, id=job_id)
    job_request.delete()  # Set approved status to False
    return redirect('admin_job_post')

@login_required
def job_status(request, alumni_id):
    alumni = get_object_or_404(Alumni, id=alumni_id)
    alumni_jobs = AlumniJob.objects.filter(alumni=alumni, approved=True)  # Fetch only approved jobs

    context = {
        'alumni': alumni,
        'alumni_jobs': alumni_jobs
    }
    return render(request, 'job_status.html', context)

@login_required
def alumni_message(request):
    return render(request, 'alumni_message.html')

@login_required
def student_message(request):   
    return render(request, 'student_message.html')