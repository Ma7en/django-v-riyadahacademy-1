# 
from django.contrib.flatpages.models import FlatPage


#
from rest_framework import serializers


# 
from accounts.serializers import *
from accounts.models import *



# 
from . import models




# ******************************************************************************
# ==============================================================================
# *** Category Section *** #
class CategorySectionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = models.CategorySection
        fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     super(CategorySectionSerializer, self).__init__(*args, **kwargs)
    #     request = self.context.get('request')
    #     if request and request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
    #         print('Method is POST')
    #         self.Meta.depth = 0
    #         print(self.Meta.depth)
    #     else:
    #         print(f"Method is - {request.method}")
    #         self.Meta.depth = 2







# ******************************************************************************
# ==============================================================================
# *** Section Course *** #
class SectionCourseSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = models.SectionCourse
        fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     super(SectionCourseSerializer, self).__init__(*args, **kwargs)
    #     request = self.context.get('request')
    #     if request and request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
    #         print('Method is POST')
    #         self.Meta.depth = 0
    #         print(self.Meta.depth)
    #     else:
    #         print(f"Method is - {request.method}")
    #         self.Meta.depth = 2







# ******************************************************************************
# ==============================================================================
# *** Course *** #
class QuestionInCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionInCourse
        fields = "__all__"


class FileInCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FileInCourse
        fields = "__all__"


class LessonInCourseSerializer(serializers.ModelSerializer):
    files = FileInCourseSerializer(many=True, read_only=True)
    questions = QuestionInCourseSerializer(many=True, read_only=True)

    class Meta:
        model = models.LessonInCourse
        fields = "__all__"


class SectionInCourseSerializer(serializers.ModelSerializer):
    items = LessonInCourseSerializer(many=True, read_only=True)

    class Meta:
        model = models.SectionInCourse
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    # section_course = SectionCourseSerializer(read_only=True)
    # section_course = SectionCourseSerializer(read_only=True, context={'request': None})
    
    sections = SectionInCourseSerializer(many=True, read_only=True)

    sections_count = serializers.IntegerField(read_only=True) 
    lessons_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = models.Course
        fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     request = self.context.get('request')
    #     if request and request.method in ['POST', 'PUT', 'PATCH']:
    #         self.Meta.depth = 0
    #     else:
    #         self.Meta.depth = 2

    # def __init__(self, *args, **kwargs):
    #         super(CourseSerializer, self).__init__(*args, **kwargs)
    #         request = self.context.get('request')
    #         if request and request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
    #             print('Method is POST')
    #             self.Meta.depth = 0
    #             print(self.Meta.depth)
    #         else:
    #             print(f"Method is - {request.method}")
    #             self.Meta.depth = 2








# ******************************************************************************
# ==============================================================================
# *** Coupon Course *** #
class CouponCourseSerializer(serializers.ModelSerializer):
    """Serializer for Coupon model (admin view)"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = models.CouponCourse
        fields = '__all__'





# ******************************************************************************
# ==============================================================================
# ***  *** #
# class TeacherDashboardSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=models.Teacher
#         fields=['total_teacher_course','total_teacher_chapters','total_teacher_students']


# class StudentDashboardSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=models.Student
#         fields=['enrolled_courses','favorite_courses','complete_assignments','pending_assignments']






# ******************************************************************************
# ==============================================================================
# *** Student Course Enroll *** #
class StudentCourseEnrollSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    course = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = models.StudentCourseEnrollment
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super(StudentCourseEnrollSerializer, self).__init__(*args, **kwargs)
    #     request = self.context.get('request')
    #     if request and request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
    #         print('Method is POST')
    #         self.Meta.depth = 0
    #         print(self.Meta.depth)
    #     else:
    #         print(f"Method is - {request.method}")
    #         self.Meta.depth = 2






# ******************************************************************************
# ==============================================================================
# *** Course Rating *** #
class CourseRatingSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    course = CourseSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.CourseRating
        fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     super(CourseRatingSerializer, self).__init__(*args, **kwargs)
    #     request = self.context.get('request')
    #     if request and request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
    #         print('Method is POST')
    #         self.Meta.depth = 0
    #         print(self.Meta.depth)
    #     else:
    #         print(f"Method is - {request.method}")
    #         self.Meta.depth = 2




# ******************************************************************************
# ==============================================================================
# *** Student Favorite Course *** #
class StudentFavoriteCourseSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)    
    course = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = models.StudentFavoriteCourse
        fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     super(StudentFavoriteCourseSerializer, self).__init__(*args, **kwargs)
    #     request = self.context.get('request')
    #     if request and request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
    #         print('Method is POST')
    #         self.Meta.depth = 0
    #         print(self.Meta.depth)
    #     else:
    #         print(f"Method is - {request.method}")
    #         self.Meta.depth = 2





# ******************************************************************************
# ==============================================================================
# *** Teacher Student Chat *** #
class TeacherStudentChatSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.TeacherStudentChat
        fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     super(TeacherStudentChatSerializer, self).__init__(*args, **kwargs)
    #     request = self.context.get('request')
    #     if request and request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
    #         print('Method is POST')
    #         self.Meta.depth = 0
    #         print(self.Meta.depth)
    #     else:
    #         print(f"Method is - {request.method}")
    #         self.Meta.depth = 3

    def to_representation(self,instance):
        representation = super(TeacherStudentChatSerializer, self).to_representation(instance)
        representation['msg_time'] = instance.msg_time.strftime("%Y-%m-%d %H:%M")
        return representation





# ******************************************************************************
# ==============================================================================
# *** Student Progress Course *** #
# class StudentProgressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.StudentProgressCourse
#         fields = '__all__'

# class CourseProgressSerializer(serializers.ModelSerializer):
#     progress = serializers.SerializerMethodField()
    
#     class Meta:
#         model = models.Course
#         fields = ['id', 'title', 'progress']
    
#     def get_progress(self, obj):
#         user = self.context['request'].user
#         progress = models.StudentProgressCourse.objects.filter(user=user, course=obj).aggregate(
#             avg_progress=models.Avg('progress_percentage')
#         )
#         return progress['avg_progress'] or 0


# ->
class LessonInCourseCompletionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    lesson = LessonInCourseSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.LessonInCourseCompletion
        fields = "__all__"


class CourseProgressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSerializer(many=True, read_only=True)
    
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_image = serializers.SerializerMethodField()
    
    class Meta:
        model = models.CourseProgress
        fields = "__all__"
    
    def get_course_image(self, obj):
        request = self.context.get('request')
        if obj.course.image:
            return request.build_absolute_uri(obj.course.image.url)
        return None
    



    

# ******************************************************************************
# ==============================================================================
# *** Student Certificate *** #
class StudentCertificateSerializer(serializers.ModelSerializer):
    enrollment = StudentCourseEnrollSerializer(many=True, read_only=True)

    course_title = serializers.CharField(source='enrollment.course.title', read_only=True)
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = models.StudentCertificate
        fields = "__all__"
    
    def get_user_name(self, obj):
        return obj.user.get_full_name()





# ******************************************************************************
# ==============================================================================
# *** Questions Banks *** #
class ChoiceQuestionInBankSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    section = SectionCourseSerializer(many=True, read_only=True)

    class Meta:
        model = models.ChoiceQuestionInBank
        # fields = ['id', 'text', 'is_correct']
        fields = "__all__"


class QuestionInBankSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # question_bank = QuestionBankListSerializer(many=True, read_only=True)

    choices = ChoiceQuestionInBankSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.QuestionInBank
        # fields = ['id', 'text', 'image', 'image_url', 'display_image', 'choices']
        fields = "__all__"


class QuestionInBankDetailSerializer(serializers.ModelSerializer):
    choices = ChoiceQuestionInBankSerializer(many=True)
    
    class Meta:
        model = models.QuestionInBank
        # fields = ['id', 'text', 'image', 'image_url', 'display_image', 'choices']
        fields = "__all__"
    
    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        question = models.QuestionInBank.objects.create(**validated_data)
        
        for choice_data in choices_data:
            models.ChoiceQuestionInBank.objects.create(question=question, **choice_data)
        
        return question
    
    def update(self, instance, validated_data):
        choices_data = validated_data.pop('choices', None)
        
        # Update question fields
        instance.text = validated_data.get('text', instance.text)
        
        instance.image = validated_data.get('image', instance.image)
        instance.image_url = validated_data.get('image_url', instance.image_url)

        instance.save()
        
        # Update choices if provided
        if choices_data is not None:
            # Delete existing choices
            instance.choices.all().delete()
            
            # Create new choices
            for choice_data in choices_data:
                models.ChoiceQuestionInBank.objects.create(question=instance, **choice_data)
        
        return instance


class QuestionBankListSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField(read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    
    class Meta:
        model = models.QuestionBank
        fields = "__all__"
        # fields = ['id', 'title', 'description', 'image', 'image_url', 
        #           'display_image', 'section', 'section_name', 'question_count']


class QuestionBankDetailSerializer(serializers.ModelSerializer):
    questions = QuestionInCourseSerializer(many=True, read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    
    class Meta:
        model = models.QuestionBank 
        fields = "__all__"
        # fields = ['id', 'title', 'description', 'image', 'image_url', 
        #           'display_image', 'section', 'section_name', 'questions']






class QuestionBankResultSerializer(serializers.Serializer): # QuizResult
    question_id = serializers.IntegerField()
    selected_choice_id = serializers.IntegerField()



class StudentQuestionBankResultSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    question_bank = QuestionBankListSerializer(many=True, read_only=True)

    class Meta:
        model = models.StudentQuestionBankResult
        fields = '__all__'
        # read_only_fields = ('user', 'created_at')


class StudentQuestionBankAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentQuestionBankAnswer
        fields = '__all__'
        extra_kwargs = {
            'all_choices': {'write_only': True}
        }








# ******************************************************************************
# ==============================================================================
# *** ContactUs *** #
class ContactUsUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.ContactUsUser
        fields = "__all__"






# ******************************************************************************
# ==============================================================================
# *** Review *** #
class ReviewUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.ReviewUser
        fields = "__all__"






# ******************************************************************************
# ==============================================================================
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










# ******************************************************************************
# ==============================================================================
# ***  *** #