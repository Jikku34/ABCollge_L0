from django.shortcuts import render, redirect
from .models import StudentInfo, StudentResult
from faculty_app.models import FacultyInfo


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# home function for check user session
def home_student(request):
    if 'user' in request.session:
        login_user = request.session['user']
        dist = FacultyInfo.objects.filter(faculty_id=login_user).values()
        if dist:
            return render(request, 'faculty_frontpage.html', {"dt": dist})
        else:
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

        check_user = StudentInfo.objects.filter(student_id=student_id, student_password=student_password,
                                                student_status="ACTIVE")

        if check_user:
            print('ddd')
            request.session['user'] = student_id
            dist = StudentInfo.objects.filter(student_id=student_id).values()
            print(dist)
            return render(request, 'student_frontpage.html', {'dt': dist})

        else:

            dt = {'dtm': 'Wrong password or User ID'}
            return render(request, 'login_student.html', dt)

    return render(request, 'login_student.html')


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# function for student result
def student_result(request):
    if 'user' in request.session:
        login_user = request.session['user']
        sem = request.POST.get('Semester')
        tpexam = request.POST.get('typeexam')
        print(sem)
        print(tpexam)
        dist = StudentResult.objects.filter(student_id=login_user, type_exam=tpexam, student_sem=sem).values()
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
                elif tpexam is None and sem != None:
                    return render(request, 'student_result.html', {"dt": 'examempty'})
                else:
                    return render(request, 'student_result.html', {"dt": 'start'})

    else:
        return redirect('student_login')
    return render(request, 'login_student.html')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# function for logout and delete session

def logout(request):
    try:
        del request.session['user']

    except:
        return redirect('student_login')
    return redirect('student_login')
