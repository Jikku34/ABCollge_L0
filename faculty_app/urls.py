from django.urls import path
from . import views

# include urls of facultyapp and studentapp
urlpatterns = [
    path('', views.home_faculty, name='home_faculty'),
    path('faculty_login', views.login, name='faculty_login'),
    path('logout/', views.logout, name='faculty_logout'),
    path('student_details', views.student_search, name="student_search"),
    path('faculty_student_profile/<str:id>', views.faculty_student_profile, name='faculty_student_profile'),
    path('clear/', views.clear, name='clear'),
    path('faculty_result', views.faculty_result, name='faculty_result'),
    path('faculty_announcement', views.faculty_announcement, name='faculty_announcement'),
    path('faculty_announcement_add', views.faculty_announcement_add, name='faculty_announcement_add'),

]
