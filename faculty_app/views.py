from django.shortcuts import render, redirect
from .models import FacultyInfo, Announcement_Model
from student_app.models import StudentInfo, StudentResult
from .encrypt_util import encrypt, decrypt, settings


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# function for home
def home_faculty(request):
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
        return redirect('faculty_login')

    return render(request, 'login_faculty.html')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# function for login faculty
def login(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('userId')
        faculty_password = request.POST.get('passWord')

        dt = FacultyInfo.objects.filter(faculty_id=faculty_id, faculty_status="ACTIVE").values()

        if dt:
            y = FacultyInfo.objects.filter(faculty_id=faculty_id).values()
            for x in y:
                prd = x.get("faculty_password")

            if decrypt(prd) == faculty_password:

                request.session['faculty_user'] = faculty_id
                dist = FacultyInfo.objects.filter(faculty_id=faculty_id).values()

                return render(request, 'faculty_frontpage.html', {'dt': dist})

            else:

                dt = {'dtm': 'Wrong password '}
                return render(request, 'login_faculty.html', dt)

        else:

            dt = {'dtm': 'Wrong User ID'}
            return render(request, 'login_faculty.html', dt)
    return render(request, 'login_faculty.html')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# function for search students in faculty in student page
def student_search(request):
    if 'faculty_user' in request.session:
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

            try:
                i = []
                for d in dist:
                    stidlist = {'id': d.get('student_id'), 'enry': encrypt(d.get('student_id'))}
                    i.append(stidlist)

            except:
                pass
            return render(request, 'faculty_student_details.html', {"dt": dist, 'list': i})

        else:
            d = searchfn(Semester, stdpt, gender)
            if d['session']:
                request.session['search'] = d['session']

            dist = d['dt']
            if dist:
                try:
                    i = []
                    for d in dist:
                        stidlist = {}
                        stidlist['id'] = d.get('student_id')
                        stidlist['enry'] = encrypt(d.get('student_id'))
                        i.append(stidlist)

                except:
                    pass
                return render(request, 'faculty_student_details.html', {"dt": dist, 'list': i})
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
    try:
        del request.session['search']

    except:
        return redirect('student_search')
    return redirect('student_search')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def faculty_student_profile(request, id):
    st_id = decrypt(id)
    dts = StudentInfo.objects.filter(student_id=st_id)
    return render(request, 'faculty_student_profile.html', {'dt': dts})


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# function for search result by faculty
def faculty_result(request):
    if 'faculty_user' in request.session:

        sem = request.POST.get('Semester')
        type_exam = request.POST.get('type_exam')
        department = request.POST.get('department')
        dist = StudentResult.objects.filter(student_dept=department, type_exam=type_exam, student_sem=sem).values()

        if sem is not None and type_exam is not None:
            if str(dist) == "<QuerySet []>":
                return render(request, 'faculty_result.html', {"dt": 'empty'})
            else:
                return render(request, 'faculty_result.html', {"dt": dist})
        else:
            if sem is None or type_exam is None or department is None:
                return render(request, 'faculty_result.html', {"dt": 'start'})

    else:
        return redirect('faculty_login')
    return render(request, 'login_faculty.html')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# faculty announcement  functions

def faculty_announcement(request):

    if 'faculty_user' in request.session:
        dist = Announcement_Model.objects.filter(announcement_faculty="Faculty").values()
        if dist:
            return render(request, 'faculty_announcement.html', {'dt': dist})
        else:
            return render(request, 'faculty_announcement.html', {'dt': 'empty'})

    else:
        return redirect('faculty_login')


def faculty_announcement_add(request):
    if 'faculty_user' in request.session:
        if request.method == 'POST':
            an_head = request.POST.get('an-head')
            an_des = request.POST.get('an-des')
            an_dpt = request.POST.get('an-dpt')
            an_sem_all = request.POST.get('an-sem_all')
            an_sem1 = request.POST.get('an-sem1')
            an_sem2 = request.POST.get('an-sem2')
            an_sem3 = request.POST.get('an-sem3')
            an_sem4 = request.POST.get('an-sem4')
            an_sem5 = request.POST.get('an-sem5')
            an_sem6 = request.POST.get('an-sem6')
            an_id = request.POST.get('an-id')
            an_date = request.POST.get('an-date')
            an_for = request.POST.get('an-for')
            an_link = request.POST.get('an-link')
            ann_data = Announcement_Model()
            ann_data.announcement_id = an_id
            ann_data.announcement_head = an_head
            ann_data.announcement_content = an_des
            ann_data.announcement_dpt = an_dpt
            ann_data.announcement_date = an_date
            ann_data.announcement_for = an_for
            ann_data.announcement_link = an_for
            ann_data.announcement_link = an_link
            if an_for == 'all-memb':
                ann_data.announcement_faculty = "Faculty"
                ann_data.announcement_student = "Student"
            elif an_for == "faculty":
                ann_data.announcement_faculty = "Faculty"
            elif an_for == 'student':
                ann_data.announcement_student = "Student"
            else:
                ann_data.announcement_faculty = None
                ann_data.announcement_student = None

            if an_sem_all:
                ann_data.announcement_S1 = "S1"
                ann_data.announcement_S2 = "S2"
                ann_data.announcement_S3 = "S3"
                ann_data.announcement_S4 = "S4"
                ann_data.announcement_S5 = "S5"
                ann_data.announcement_S6 = "S6"
            else:
                ann_data.announcement_S1 = an_sem1
                ann_data.announcement_S2 = an_sem2
                ann_data.announcement_S3 = an_sem3
                ann_data.announcement_S4 = an_sem4
                ann_data.announcement_S5 = an_sem5
                ann_data.announcement_S6 = an_sem6
            ann_data.save()
        return render(request, 'faculty_announcement_add.html', )

    else:
        return redirect('faculty_login')


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# function for logout and delete session

def logout(request):
    try:
        del request.session['faculty_user']

    except:
        return redirect('faculty_login')
    return redirect('faculty_login')
