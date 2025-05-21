# 
from django.contrib.flatpages.models import FlatPage


#
from rest_framework import serializers


# 
from cores import models


# *****************************************************************
# =================================================================
# *** Category Section *** #
class CategorySectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CategorySection
        fields = "__all__"

    def __init__(self, *args, **kwargs):
            super(CategorySectionSerializer, self).__init__(*args, **kwargs)
            request = self.context.get('request')
            if request and request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
                print('Method is POST')
                self.Meta.depth = 0
                print(self.Meta.depth)
            else:
                print(f"Method is - {request.method}")
                self.Meta.depth = 2


# *****************************************************************
# =================================================================
# *** Section Course *** #
class SectionCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SectionCourse
        fields = "__all__"

    def __init__(self, *args, **kwargs):
            super(SectionCourseSerializer, self).__init__(*args, **kwargs)
            request = self.context.get('request')
            if request and request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
                print('Method is POST')
                self.Meta.depth = 0
                print(self.Meta.depth)
            else:
                print(f"Method is - {request.method}")
                self.Meta.depth = 2



# *****************************************************************
# =================================================================
# *** Course *** #

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = "__all__"


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = models.Item
        fields = "__all__"

class SectionSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.Section
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    sections_count = serializers.IntegerField(read_only=True)
    # students_count = serializers.IntegerField(read_only=True)
    lessons_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = models.Course
        fields = "__all__"

    def __init__(self, *args, **kwargs):
            super(CourseSerializer, self).__init__(*args, **kwargs)
            request = self.context.get('request')
            if request and request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
                print('Method is POST')
                self.Meta.depth = 0
                print(self.Meta.depth)
            else:
                print(f"Method is - {request.method}")
                self.Meta.depth = 2



# *****************************************************************
# =================================================================
# ***  *** #
# class TeacherDashboardSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=models.Teacher
#         fields=['total_teacher_course','total_teacher_chapters','total_teacher_students']


# class StudentDashboardSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=models.Student
#         fields=['enrolled_courses','favorite_courses','complete_assignments','pending_assignments']





# *****************************************************************
# =================================================================
# *** Student Course Enroll *** #
class StudentCourseEnrollSerializer(serializers.ModelSerializer):        
        class Meta:
            model = models.StudentCourseEnrollment
            fields = '__all__'

        def __init__(self, *args, **kwargs):
            super(StudentCourseEnrollSerializer, self).__init__(*args, **kwargs)
            request = self.context.get('request')
            if request and request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
                print('Method is POST')
                self.Meta.depth = 0
                print(self.Meta.depth)
            else:
                print(f"Method is - {request.method}")
                self.Meta.depth = 2




# *****************************************************************
# =================================================================
# *** Course Rating *** #
class CourseRatingSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.CourseRating
            fields = "__all__"

        def __init__(self, *args, **kwargs):
            super(CourseRatingSerializer, self).__init__(*args, **kwargs)
            request = self.context.get('request')
            if request and request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
                print('Method is POST')
                self.Meta.depth = 0
                print(self.Meta.depth)
            else:
                print(f"Method is - {request.method}")
                self.Meta.depth = 2



# *****************************************************************
# =================================================================
# *** Student Favorite Course *** #
class StudentFavoriteCourseSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.StudentFavoriteCourse
            fields = "__all__"

        def __init__(self, *args, **kwargs):
            super(StudentFavoriteCourseSerializer, self).__init__(*args, **kwargs)
            request = self.context.get('request')
            if request and request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
                print('Method is POST')
                self.Meta.depth = 0
                print(self.Meta.depth)
            else:
                print(f"Method is - {request.method}")
                self.Meta.depth = 2



# *****************************************************************
# =================================================================
# *** Teacher Student Chat *** #
class TeacherStudentChatSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.TeacherStudentChat
        fields = "__all__"

        def __init__(self, *args, **kwargs):
            super(TeacherStudentChatSerializer, self).__init__(*args, **kwargs)
            request = self.context.get('request')
            if request and request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
                print('Method is POST')
                self.Meta.depth = 0
                print(self.Meta.depth)
            else:
                print(f"Method is - {request.method}")
                self.Meta.depth = 3

        def to_representation(self,instance):
            representation=super(TeacherStudentChatSerializer, self).to_representation(instance)
            representation['msg_time']=instance.msg_time.strftime("%Y-%m-%d %H:%M")
            return representation



# *****************************************************************
# =================================================================
# *** ContactUs *** #
class ContactUsUserSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.ContactUsUser
        fields = "__all__"




# *****************************************************************
# =================================================================
# *** Review *** #
class ReviewUserSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.ReviewUser
        fields = "__all__"




# *****************************************************************
# =================================================================
# ***  *** #
# class CategoryPostSerializer(serializers.ModelSerializer):
#     slug = serializers.SlugField(read_only=True)
#     view = serializers.IntegerField(read_only=True)
#     likes_count = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = models.Category
#         fields = "__all__"

#     def get_likes_count(self, obj):
#         return obj.likes.count()

# class PostSerializer(serializers.ModelSerializer):
#     likes_count = serializers.SerializerMethodField(read_only=True)
#     slug = serializers.SlugField(read_only=True)
#     view = serializers.IntegerField(read_only=True)

#     class Meta:
#         model = models.Post
#         fields = "__all__"
    
#     def get_likes_count(self, obj):
#         return obj.likes.count()
    
# class CommentSerializer(serializers.ModelSerializer):
#     likes_count = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = models.Comment
#         fields = "__all__"
    
#     def get_likes_count(self, obj):
#         return obj.likes.count()
    
# class ReplySerializer(serializers.ModelSerializer):
#     likes_count = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = models.Reply
#         fields = "__all__"

#     def get_likes_count(self, obj):
#         return obj.likes.count()

# class NotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Notification
#         fields = "__all__"

# class ReportSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Report
#         fields = "__all__"


# *****************************************************************
# =================================================================
# ***  *** #