"""
URL configuration for alumini_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from alumini import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register_student/', views.register_student, name='register_student'),
    path('register_alumini/', views.register_alumini, name='register_alumini'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('change_password/<int:user_id>/', views.change_password, name='change_password'),  # For student

    path('admin_course/', views.admin_course, name='admin_course'),
    path('users_list/', views.users_list, name='users_list'),
    path('delete_user/<str:email>/', views.delete_user, name='delete_user'),
    path('user_request/', views.user_request, name='user_request'),
    path('approve_student/<int:student_id>/', views.approve_student, name='approve_student'),
    path('approve_alumni/<int:alumni_id>/', views.approve_alumni, name='approve_alumni'),
    path('reject_student/<int:student_id>/', views.reject_student, name='reject_student'),
    path('reject_alumni/<int:alumni_id>/', views.reject_alumni, name='reject_alumni'),

    path('student_index/', views.student_index, name='student_index'),
    path('alumni_index/', views.alumni_index, name='alumni_index'),

    path('admin_events/', views.admin_events, name='admin_events'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)