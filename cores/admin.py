# 
from django.contrib import admin


# 
from . import models




# ******************************************************************************
# ==============================================================================
# *** Course *** #
admin.site.register(models.CategorySection)
admin.site.register(models.SectionCourse)
admin.site.register(models.Course)
admin.site.register(models.SectionInCourse)
admin.site.register(models.ItemInCourse)
admin.site.register(models.FileInCourse)
admin.site.register(models.QuestionInCourse)
admin.site.register(models.Course)

admin.site.register(models.StudentCourseEnrollment)
admin.site.register(models.CourseRating)
admin.site.register(models.StudentFavoriteCourse)

admin.site.register(models.TeacherStudentChat)




# ******************************************************************************
# ==============================================================================
# *** Question Bank *** #
# admin.site.register(models.QuestionBank)
# admin.site.register(models.QuestionInBank)
# admin.site.register(models.ChoiceQuestionInBank) 

# 
class ChoiceInline(admin.TabularInline):
    model = models.ChoiceQuestionInBank
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text', 'question_bank')
    search_fields = ('text',)
    list_filter = ('question_bank',)

class QuestionInline(admin.TabularInline):
    model = models.QuestionInBank
    extra = 0
    show_change_link = True

class QuestionBankAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'section', 'question_count', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('section',)
 
admin.site.register(models.QuestionBank, QuestionBankAdmin)
admin.site.register(models.QuestionInBank, QuestionAdmin)
admin.site.register(models.ChoiceQuestionInBank)




# ******************************************************************************
# ==============================================================================
# *** Contact & Review *** #
admin.site.register(models.ContactUsUser)
admin.site.register(models.ReviewUser)





# ******************************************************************************
# ==============================================================================
# admin.site.register(models.Post)
# admin.site.register(models.Comment)
# admin.site.register(models.Reply)
# admin.site.register(models.Notification)
# admin.site.register(models.Report)






# ******************************************************************************
# ==============================================================================