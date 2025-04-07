
from django.urls import path
from . import  views

urlpatterns = [
    
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('contact/', views.contact, name="contact"),
    path('view_feedbacks/', views.view_feedbacks, name='feedbacks'),
    path('about/', views.about, name="about"),
    path('login_view/', views.login_view, name="login_view"),
    path('admin_login/', views.admin_login_view, name="admin_login"),
    path('admin_dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    # path('create_test/', views.generate_mcqs_for_topic, name='create_test'),
    path('create_test/', views.mcq_test, name='create_test'),
    path('submit_test/', views.submit_test, name='submit_test'),
    path('logout/', views.user_logout, name='logout'), 
    path('user_dashboard/', views.user_dashboard, name="user_dashboard"),
    path('current_course/', views.current_course, name="current_course"),
    path('python_course/', views.python_course, name="python_course"),
    path('java_course/', views.java_course, name="java_course"),
    path('cpp_course/', views.cpp_course, name="cpp_course"),
    path('dbms_course/', views.dbms_course, name="dbms_course"),
    path('os_course/', views.os_course, name="os_course"),
    path('networking_course/', views.networking_course, name="networking_course"),
    path('devops_course/', views.devops_course, name="devops_course"),
    path("generate_pdf/", views.generate_pdf, name="generate_pdf"),
]

