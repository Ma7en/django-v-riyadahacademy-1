# 
from django.contrib import admin


# 
from . import models

# ==============================================================================
admin.site.register(models.CategorySection)
admin.site.register(models.SectionCourse)
admin.site.register(models.Course)
admin.site.register(models.Section)
admin.site.register(models.Item)
admin.site.register(models.File)
admin.site.register(models.Question)
admin.site.register(models.Course)

admin.site.register(models.StudentCourseEnrollment)
admin.site.register(models.CourseRating)
admin.site.register(models.StudentFavoriteCourse)

admin.site.register(models.TeacherStudentChat)

# ==============================================================================
admin.site.register(models.ContactUsUser)
admin.site.register(models.ReviewUser)

# ==============================================================================
# admin.site.register(models.Post)
# admin.site.register(models.Comment)
# admin.site.register(models.Reply)
# admin.site.register(models.Notification)
# admin.site.register(models.Report)

