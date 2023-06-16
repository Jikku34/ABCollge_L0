from django.shortcuts import render, redirect
from .models import StudentInfo, StudentResult
from faculty_app.models import FacultyInfo, Announcement_Model
from faculty_app.encrypt_util import encrypt, decrypt, settings


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# home function for check user session
def home_student(request):
    if 'faculty_user' in request.session or 'student_user' in request.session:
        if 'faculty_user' in request.session:
            login_user = request.session['faculty_user']
            dist = FacultyInfo.objects.filter(faculty_id=login_user).values()
            return render(request, 'faculty_frontpage.html', {'dt': dist})
        else:
            login_user = request.session['student_user']
            dist = StudentInfo.objects.filter(student_id=login_user).values()
            return render(request, 'student_frontpage.html', {"dt": dist})

    else:
        return redirect('student_login')

    return render(request, 'login_student.html')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# function for login student

def login(request):
    if request.method == 'POST':
        student_id = request.POST.get('userId')
        student_password = request.POST.get('passWord')
        print(student_password)
        dt = StudentInfo.objects.filter(
            student_id=student_id, student_status="ACTIVE").values()

        if dt:
            y = StudentInfo.objects.filter(student_id=student_id).values()
            for x in y:
                pad = x.get("student_password")
            print(pad)

            if decrypt(pad) == student_password:

                request.session['student_user'] = student_id

                dst = StudentInfo.objects.filter(
                    student_id=student_id).values()

                return render(request, 'student_frontpage.html', {'dt': dst})

            else:

                dt = {'dtm': 'Wrong password '}
                return render(request, 'login_student.html', dt)

        else:

            dt = {'dtm': 'Wrong User ID'}
            return render(request, 'login_student.html', dt)

    return render(request, 'login_student.html')


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# function for student result
def student_result(request):
    if 'student_user' in request.session:
        login_user = request.session['student_user']
        sem = request.POST.get('Semester')
        tpexam = request.POST.get('typeexam')
        print(sem)
        print(tpexam)
        dist = StudentResult.objects.filter(
            student_id=login_user, type_exam=tpexam, student_sem=sem).values()
        print(str(dist))
        if sem is not None and tpexam is not None:
            if str(dist) == "<QuerySet []>":
                return render(request, 'student_result.html', {"dt": 'empty'})
            else:
                return render(request, 'student_result.html', {"dt": dist})
        else:
            if sem is None or tpexam is None:
                if sem is None and tpexam is not None:
                    return render(request, 'student_result.html', {"dt": 'semempty'})
                elif tpexam is None and sem is not None:
                    return render(request, 'student_result.html', {"dt": 'examempty'})
                else:
                    return render(request, 'student_result.html', {"dt": 'start'})

    else:
        return redirect('student_login')
    return render(request, 'login_student.html')


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  function for student announcement
def student_announcement(request):
    global z
    if 'student_user' in request.session:
        login_user = request.session['student_user']
        data = StudentInfo.objects.filter(student_id=login_user).values()

        for x in data:
            y = x['student_sem']
            z=x['student_dept']
        data_ann=Announcement_Model.objects.filter(announcement_student="Student",announcement_dpt=z).values()
        if data_ann:
            print("y")
            return render(request, 'student_anncouncement1.html', {'dt': data_ann,'st_sem':y})
        else:
            print("x")
            return render(request, 'student_anncouncement1.html', {'dt': 'empty'})


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# function for logout and delete session

def logout(request):
    try:
        del request.session['student_user']

    except:
        return redirect('student_login')
    return redirect('student_login')
