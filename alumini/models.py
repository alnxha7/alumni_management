from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=255, unique=True)  # Field to store the course title

    def __str__(self):
        return self.title
    
class Student(models.Model):
    adnum = models.CharField(max_length=20, unique=True)  # Admission number
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # ForeignKey to Course
    number = models.CharField(max_length=15)  # Phone number
    email = models.EmailField(unique=True)  # Unique email address
    password = models.CharField(max_length=128)  # Password field
    image = models.ImageField(upload_to='student_images/')  # Directory for storing images
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Alumni(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # ForeignKey to Course
    passout = models.IntegerField()  # Year of passing out
    number = models.CharField(max_length=15)  # Phone number
    email = models.EmailField(unique=True)  # Unique email address
    password = models.CharField(max_length=128)  # Password field
    image = models.ImageField(upload_to='alumni_images/')  # Directory for storing images
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Events(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200) 
    date = models.DateField()
    venue = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class AlumniJob(models.Model):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name="jobs")  
    company_name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    date_joined = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2) 
    image = models.ImageField(upload_to='alumni_job_images/') 
    approved = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.company_name} - {self.role} ({self.alumni.name})"
    
class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='sent_messages')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recieved_messages')
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
