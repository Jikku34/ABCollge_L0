
from django.urls import path
from . import views
# include urls of facultyapp and studentapp
urlpatterns = [
    path('', views.home_faculty, name='home_faculty'),
    path('faculty_login', views.login, name='faculty_login'),
    path('logout/', views.logout, name='faculty_logout'),
    path( 'student' , views.student_search, name="student_search"),
    path('faculty_student_profile/<str:id>', views.faculty_student_profile, name='faculty_student_profile'),
    path('clear/',views.clear,name='clear'),


]