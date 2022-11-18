"""AttendanceManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from . import views


urlpatterns = [
    path('logout/', views.logoutUser,name='logout'),
    path('login/', views.loginPage,name='login'),
    path('register/', views.registerPage,name='register'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('admin/', admin.site.urls),
    path('home/', views.home,name='home'),
    path('addImage/<str:id>',views.addImages, name='addImage'),
    path('trainModel/',views.trainModel, name='trainModel'),
    path('detectFaces/<str:course>',views.detectFaces, name='detectFaces'),
    path('addSample/',views.addSample, name='addSample'),
    path('courseOption/',views.courseOption, name='courseOption'),
    path('getAttendance/<str:course_id>/<str:roll_no>',views.getAttendance, name='getAttendance'),
    path('getCourses/<str:roll_no>',views.getCourses, name='getCourses'),
    path('getDetailAttendance/<str:roll_no>/<str:course_id>',views.getDetailAttendance,name='getDetailAttendance')
]
