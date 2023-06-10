from django.urls import path
from . import views

# include urls of facultyapp and studentapp
urlpatterns = [
    path('', views.home_student, name='student_home'),
    path('student_login/', views.login, name='student_login'),
    path('logout/', views.logout, name='student_logout'),
    path('student_result/', views.student_result, name='student_result'),

]