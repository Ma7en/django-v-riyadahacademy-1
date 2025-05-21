#
from django.contrib import admin


#
from accounts import models


# Register your models here.
admin.site.register(models.User)
admin.site.register(models.AdminProfile)
admin.site.register(models.TeacherProfile)
admin.site.register(models.StaffProfile)
admin.site.register(models.StudentProfile)
admin.site.register(models.OneTimeOTP)
