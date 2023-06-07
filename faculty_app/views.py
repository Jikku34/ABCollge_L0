from django.shortcuts import render, redirect
from .models import FacultyInfo
from student_app.models import StudentInfo


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# function for home
def home_faculty(request):
    if 'user' in request.session:
        login_user = request.session['user']
        dist = FacultyInfo.objects.filter(faculty_id=login_user).values()
        print("kkk")
        print(dist)
        if dist:
            print("aaa")
            return render(request, 'faculty_frontpage.html', {"dt": dist})
        else:
            dist = StudentInfo.objects.filter(student_id=login_user).values()
            return render(request, 'student_frontpage.html', {"dt": dist})

    else:
        return redirect('faculty_login')

    return render(request, 'login_faculty.html')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# function for login faculty

def login(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('userId')
        faculty_password = request.POST.get('passWord')

        check_user = FacultyInfo.objects.filter(faculty_id=faculty_id, faculty_password=faculty_password,
                                                faculty_status="ACTIVE")

        if check_user:
            print('ddd')
            request.session['user'] = faculty_id
            dist = FacultyInfo.objects.filter(faculty_id=faculty_id).values()
            print(dist)
            return render(request, 'faculty_frontpage.html', )

        else:

            dt = {'dtm': 'Wrong password or User ID'}
            return render(request, 'login_faculty.html', dt)
    return render(request, 'login_faculty.html')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# function for search students in faculty in student page
def student_search(request):
    if 'user' in request.session:
        Semester = request.POST.get('Semester')
        stdpt = request.POST.get('stdpt')
        gender = request.POST.get('gender')
        if 'search' in request.session and Semester is None and stdpt is None and gender is None:
            search = request.session['search']

            A = search
            i = 0
            d = []
            while i < len(A):
                d.append(A[i:i + 2])
                i = i + 2
            print(d[0])
            if d[0] == "NA":
                Semester = None
            else:
                Semester = d[0]
            if d[1] == "NA":
                stdpt = None
            else:
                stdpt = d[1]
            if d[2] == "NA":
                gender = None
            else:
                gender = d[2]

            d = searchfn(Semester, stdpt, gender)
            dist = d['dt']
            for d in dist:
                print((d['student_id']))
            return render(request, 'faculty_student_details.html', {"dt": dist})

        else:
            d = searchfn(Semester, stdpt, gender)
            if d['session']:
                request.session['search'] = d['session']

            dist = d['dt']
            if dist:
                for d in dist:
                    print(d['student_id'])
                return render(request, 'faculty_student_details.html', {"dt": dist})
            else:
                return render(request, 'faculty_student_details.html', {"dt": 'start'})

        # return render(request, 'homepage.html', {"dt": 'start'})
    else:
        return redirect('faculty_login')
    # return render(request, 'login_faculty.html')


# _________________________________________________________________________________________________
def stdptfn(stdpt):
    if stdpt == "ME":
        dpt = "MECHANICAL ENGINEERING"
    elif stdpt == "EC":
        dpt = "ELECTRONICS AND COMMUNICATION"
    elif stdpt == "CS":
        dpt = "COMPUTER SCIENCE"
    elif stdpt == "EE":
        dpt = "ELECTRICAL ENGINEERING"
    else:
        dpt = "CIVIL ENGINEERING"
    return dpt


def genderfn(gender):
    if gender == "FG":
        g = "FEMALE"
    else:
        g = "MALE"
    return g


# search fun for search students  in fun student_search()
def searchfn(Semester, stdpt, gender):
    if Semester is None and stdpt is not None and gender is not None:
        c = "NA" + stdpt + gender
        dist = StudentInfo.objects.filter(student_dept=stdptfn(stdpt), student_gender=genderfn(gender)).values()

    elif Semester is None and stdpt is None and gender is not None:
        c = "NANA" + gender
        dist = StudentInfo.objects.filter(student_gender=genderfn(gender)).values()

    elif Semester is None and stdpt is not None and gender is None:
        c = "NA" + stdpt + "NA"
        dist = StudentInfo.objects.filter(student_dept=stdptfn(stdpt)).values()
        print(str(dist))

    # ++++++++++++++++++++++++++++++++++++++++++++++++++
    elif stdpt is None and Semester is not None and gender is not None:
        c = Semester + "NA" + gender
        dist = StudentInfo.objects.filter(student_sem=Semester, student_gender=genderfn(gender)).values()

    elif stdpt is None and Semester is None and gender is not None:
        c = "NANA" + gender
        dist = StudentInfo.objects.filter(student_gender=genderfn(gender)).values()

    elif stdpt is None and Semester is not None and gender is None:
        c = Semester + "NANA"
        dist = StudentInfo.objects.filter(student_sem=Semester).values()

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    elif stdpt is not None and Semester is not None and gender is None:
        c = Semester + stdpt + "NA"
        dist = StudentInfo.objects.filter(student_dept=stdptfn(stdpt), student_sem=Semester).values()

    elif stdpt is None and Semester is not None and gender is None:
        c = Semester + "NANA"
        dist = StudentInfo.objects.filter(student_sem=Semester).values()

    elif stdpt is not None and Semester == None and gender is None:
        c = Semester + "NANA"
        dist = StudentInfo.objects.filter(student_dept=stdptfn(stdpt)).values()

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    elif stdpt is not None and Semester is not None and gender is not None:
        c = Semester + stdpt + gender
        dist = StudentInfo.objects.filter(student_dept=stdptfn(stdpt), student_sem=Semester,
                                          student_gender=genderfn(gender)).values()

    else:
        dist = StudentInfo.objects.filter(student_dept=stdpt, student_sem=Semester, student_gender=gender).values()
        c = None
    return {'session': c, 'dt': dist}


def clear(request):
    print("clear success")
    try:
        del request.session['search']

    except:
        return redirect('student_search')
    return redirect('student_search')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def faculty_student_profile(request, id):
    dts = StudentInfo.objects.filter(student_id=id)
    # for d in dts:
    #     print(type(d['student_id']))
    print("lll")
    print(dts)
    return render(request, 'faculty_student_profile.html', {'dt': dts})


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# function for logout and delete session

def logout(request):
    try:
        del request.session['user']

    except:
        return redirect('faculty_login')
    return redirect('faculty_login')



