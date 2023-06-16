from django.db import models


# Model for the faculty information

class FacultyInfo(models.Model):
    faculty_name = models.CharField(max_length=100, null=True)
    faculty_id = models.CharField(max_length=100, null=True)
    faculty_gender = models.CharField(max_length=100, null=True)
    faculty_position = models.CharField(max_length=100, null=True)
    faculty_code = models.CharField(max_length=100, null=True)
    faculty_email = models.EmailField(null=True)
    faculty_aadhar = models.CharField(max_length=100, null=True)
    faculty_phone = models.CharField(max_length=250, null=True)
    faculty_address = models.CharField(max_length=250, null=True)
    faculty_dept = models.CharField(max_length=100, null=True)
    faculty_year_join = models.DateField(null=True)
    faculty_password = models.CharField(max_length=400, null=True)
    faculty_status = models.CharField(max_length=100, null=True)
    faculty_dob = models.DateField(null=True)
    faculty_image = models.ImageField(upload_to='images/', null=True)

    class Meta:
        db_table = "faculty_info_table"

    def __str__(self):
        return self.faculty_id


# Model for the message

class Message_Model(models.Model):
    sender_id = models.CharField(max_length=50, null=True)
    receiver_id = models.CharField(max_length=50, null=True)
    message = models.CharField(max_length=500, null=True)
    message_date = models.DateTimeField(null=True)

    class Meta:
        db_table = "message_table"

    def __str__(self):
        return self.sender_id, self.receiver_id


class Announcement_Model(models.Model):
    announcement_head = models.CharField(max_length=50, null=True)
    announcement_content = models.CharField(max_length=550, null=True)
    announcement_id = models.CharField(max_length=50, null=True)
    announcement_student = models.CharField(max_length=50, null=True)
    announcement_faculty = models.CharField(max_length=50, null=True)
    announcement_link = models.CharField(max_length=250, null=True)
    announcement_dpt = models.CharField(max_length=50, null=True)
    # announcement_sem = models.JSONField(null=True)
    announcement_date = models.DateTimeField(null=True)
    announcement_S1 = models.CharField(max_length=50, null=True)
    announcement_S2 = models.CharField(max_length=50, null=True)
    announcement_S3 = models.CharField(max_length=50, null=True)
    announcement_S4 = models.CharField(max_length=50, null=True)
    announcement_S5 = models.CharField(max_length=50, null=True)
    announcement_S6 = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "ann_info_table"

    def __str__(self):
        return self.announcement_id
