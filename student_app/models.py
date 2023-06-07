from django.db import models


# Models for Student Information's


class StudentInfo(models.Model):

    student_name = models.CharField(max_length=100, null=True)
    student_gender = models.CharField(max_length=100, null=True)
    student_id = models.CharField(max_length=100, null=True)
    student_sem = models.CharField(max_length=100, null=True)
    student_div = models.CharField(max_length=100, null=True)
    student_code = models.CharField(max_length=100, null=True)
    student_aadhar = models.CharField(max_length=100, null=True)
    student_email = models.EmailField(null=True)
    student_phone = models.CharField(max_length=250, null=True)
    student_address = models.CharField(max_length=250, null=True)
    student_dept = models.CharField(max_length=100, null=True)
    student_year_join = models.DateField(null=True)
    student_password = models.CharField(max_length=400, null=True)
    student_status = models.CharField(max_length=100, null=True)
    student_dob = models.DateField(null=True)
    student_image = models.ImageField(upload_to='images/',null=True)

    class Meta:
        db_table = "student_info_table"

    def __str__(self):
        return self.student_id


# Models for student result

class StudentResult(models.Model):
    student_id = models.CharField(max_length=100, null=True)
    student_sem = models.CharField(max_length=100, null=True)
    exam_code = models.CharField(max_length=100, null=True)
    type_exam = models.CharField(max_length=100, null=True)
    exam_date = models.DateField(null=True)
    result_date = models.DateField(null=True)
    subject1 = models.IntegerField(null=True)
    subject2 = models.IntegerField(null=True)
    subject3 = models.IntegerField(null=True)
    subject4 = models.IntegerField(null=True)
    subject5 = models.IntegerField(null=True)
    subject6 = models.IntegerField(null=True)
    subject7 = models.IntegerField(null=True)
    subject8 = models.IntegerField(null=True)
    subject9 = models.IntegerField(null=True)
    subject10 = models.IntegerField(null=True)
    exam_status = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "student_result_table"

    def __str__(self):
        return self.student_id
