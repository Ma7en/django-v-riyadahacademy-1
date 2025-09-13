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
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 

    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.CategorySection
        # fields = "__all__"
        fields = [
            "id",

            "user", 
            
            "title", 
            "description", 
            "image", 
            "image_url", 
            "is_visible", 
            
            "slug", 
            "created_at",
            "updated_at",
            
            "total_section_course",
            ]
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # لعرض تفاصيل المستخدم
        return representation
    
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
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    category = serializers.PrimaryKeyRelatedField(queryset=models.CategorySection.objects.all()) 

    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.SectionCourse
        # fields = "__all__"
        fields = [
            "id",

            "user", 
            "category",
            
            "title",
            "description",
            "grade",
            "image",
            "image_url",
            "is_visible", 
            
            "slug", 
            "created_at",
            "updated_at",

            "total_course",
            "total_question_bank",
            ]
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # لعرض تفاصيل المستخدم
        representation['category'] = CategorySectionSerializer(instance.category).data  # لعرض تفاصيل المستخدم
        return representation
    

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
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.QuestionInCourse
        fields = "__all__"


class FileInCourseSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.FileInCourse
        fields = "__all__"


class LessonInCourseSerializer(serializers.ModelSerializer):
    files = FileInCourseSerializer(many=True, read_only=True)
    # questions = QuestionInCourseSerializer(many=True, read_only=True)

    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.LessonInCourse
        fields = "__all__"


class SectionInCourseSerializer(serializers.ModelSerializer):
    # items = LessonInCourseSerializer(many=True, read_only=True)
    lessons = LessonInCourseSerializer(
        many=True, 
        read_only=True, 
        source='section_lesson'  # يستخدم related_name الموجود في الموديل
    )

    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.SectionInCourse
        # fields = "__all__"
        fields = [
            "id",

            "course",

            "title",
            "is_visible",
            "is_free",
            "order",

            # 
            "lessons",

            "slug", 
            "created_at",
            "updated_at",

            "total_lesson",
        ]


class CourseSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    section = serializers.PrimaryKeyRelatedField(queryset=models.SectionCourse.objects.all())

    # section_course = SectionCourseSerializer(read_only=True)
    # section_course = SectionCourseSerializer(read_only=True, context={'request': None})
    
    # sections = SectionInCourseSerializer(many=True, read_only=True)
    sections = SectionInCourseSerializer(
        many=True, 
        read_only=True, 
        source='course_sections'  # يستخدم related_name الموجود في الموديل
    )

    slug = serializers.SlugField(read_only=True)
    
    class Meta:
        model = models.Course
        # fields = "__all__"
        fields = [
            "id",
            
            "user",
            "section",

            "level",
            "title",
            "description",
            "image",
            "image_url",
            "duration",
            "price",
            "discount",
            "rating",
            "reviews_count",
            "students_count",
            "language",
            "tag",
            "techs",
            "features",
            "requirements",
            "target_audience",
            "is_visible",

            # 
            "sections",

            "slug",
            "created_at",
            "updated_at",

            "teach_list",
            "total_section",
            "total_lesson",
            "total_enrolled_students",
            "course_rating",
            "price_after_discount",
        ]
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # لعرض تفاصيل المستخدم
        representation['section'] = SectionCourseSerializer(instance.section).data  # لعرض تفاصيل المستخدم
        return representation
    

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



class CourseNotAllSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    section = serializers.PrimaryKeyRelatedField(queryset=models.SectionCourse.objects.all())


    slug = serializers.SlugField(read_only=True)
    
    class Meta:
        model = models.Course
        # fields = "__all__"
        fields = [
            "id",
            
            "user",
            "section",

            "level",
            "title",
            "description",
            "image",
            "image_url",
            "duration",
            "price",
            "discount",
            "rating",
            "reviews_count",
            "students_count",
            "language",
            "tag",
            "techs",
            "features",
            "requirements",
            "target_audience",
            "is_visible",

            # 
            # "sections",

            "slug",
            "created_at",
            "updated_at",

            "teach_list",
            "total_section",
            "total_lesson",
            "total_enrolled_students",
            "course_rating",
            "price_after_discount",
        ]
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # لعرض تفاصيل المستخدم
        representation['section'] = SectionCourseSerializer(instance.section).data  # لعرض تفاصيل المستخدم
        return representation
    




# ******************************************************************************
# ==============================================================================
# *** Coupon Course *** #
class CouponCourseSerializer(serializers.ModelSerializer):
    """Serializer for Coupon model (admin view)"""
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    
    slug = serializers.SlugField(read_only=True)
  
    class Meta:
        model = models.CouponCourse
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # لعرض تفاصيل المستخدم
        return representation




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
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    course = serializers.PrimaryKeyRelatedField(queryset=models.Course.objects.all()) 
  
    slug = serializers.SlugField(read_only=True)
  
    class Meta:
        model = models.StudentCourseEnrollment
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['student'] = UserSerializer(instance.student).data  # لعرض تفاصيل المستخدم
        representation['course'] = CourseSerializer(instance.course).data  # لعرض تفاصيل المستخدم
        return representation
    
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


class StudentCourseNotAllEnrollSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    course = serializers.PrimaryKeyRelatedField(queryset=models.Course.objects.all()) 
  
    slug = serializers.SlugField(read_only=True)
  
    class Meta:
        model = models.StudentCourseEnrollment
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['student'] = UserSerializer(instance.student).data  # لعرض تفاصيل المستخدم
        representation['course'] = CourseNotAllSerializer(instance.course).data  # لعرض تفاصيل المستخدم
        return representation



# ******************************************************************************
# ==============================================================================
# *** Course Rating *** #
class CourseRatingSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    course = serializers.PrimaryKeyRelatedField(queryset=models.Course.objects.all()) 
    
    slug = serializers.SlugField(read_only=True)
  
    class Meta:
        model = models.CourseRating
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['student'] = UserSerializer(instance.student).data  # لعرض تفاصيل المستخدم
        representation['course'] = CourseSerializer(instance.course).data  # لعرض تفاصيل المستخدم
        return representation
    

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
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())     
    course = serializers.PrimaryKeyRelatedField(queryset=models.Course.objects.all())     

    slug = serializers.SlugField(read_only=True)
  

    class Meta:
        model = models.StudentFavoriteCourse
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['student'] = UserSerializer(instance.student).data  # لعرض تفاصيل المستخدم
        representation['course'] = CourseSerializer(instance.course).data  # لعرض تفاصيل المستخدم
        return representation
    
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

    def to_representation(self,instance):
        representation = super(TeacherStudentChatSerializer, self).to_representation(instance)
        representation['msg_time'] = instance.msg_time.strftime("%Y-%m-%d %H:%M")
        return representation

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
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    lesson = serializers.PrimaryKeyRelatedField(queryset=models.LessonInCourse.objects.all()) 
    
    slug = serializers.SlugField(read_only=True)
  
    class Meta:
        model = models.LessonInCourseCompletion
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # لعرض تفاصيل المستخدم
        representation['lesson'] = LessonInCourseSerializer(instance.lesson).data  # لعرض تفاصيل المستخدم
        return representation
    

class CourseProgressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    course = serializers.PrimaryKeyRelatedField(queryset=models.Course.objects.all()) 
    
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_image = serializers.SerializerMethodField()
    
    slug = serializers.SlugField(read_only=True)
  
    class Meta:
        model = models.CourseProgress
        fields = "__all__"
    
    def get_course_image(self, obj):
        request = self.context.get('request')
        if obj.course.image:
            return request.build_absolute_uri(obj.course.image.url)
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # لعرض تفاصيل المستخدم
        representation['course'] = UserSerializer(instance.course).data  # لعرض تفاصيل المستخدم
        return representation    



    

# ******************************************************************************
# ==============================================================================
# *** Student Certificate *** #
class StudentCertificateSerializer(serializers.ModelSerializer):
    # enrollment = StudentCourseEnrollSerializer(many=True, read_only=True)
    enrollment = serializers.PrimaryKeyRelatedField(queryset=models.StudentCourseEnrollment.objects.all()) 

    course_title = serializers.CharField(source='enrollment.course.title', read_only=True)
    user_name = serializers.SerializerMethodField()
    
    slug = serializers.SlugField(read_only=True)
  
    class Meta:
        model = models.StudentCertificate
        fields = "__all__"
    
    def get_user_name(self, obj):
        return obj.user.get_full_name()
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['enrollment'] = StudentCourseEnrollSerializer(instance.enrollment).data  # لعرض تفاصيل المستخدم 
        return representation   


# ******************************************************************************
# ==============================================================================
# ***  Subscribe Course   *** #
class SubscribeCourseSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    course = serializers.PrimaryKeyRelatedField(queryset=models.Course.objects.all()) 
    coupon_course = serializers.PrimaryKeyRelatedField(queryset=models.CouponCourse.objects.all()) 
    # course = CourseSerializer() 

    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.SubscribeCourse
        # fields = "__all__"
        fields = [
            "id",
            
            "user",
            "course",
            "coupon_course",

            "status",
            "image_url",
            "full_name",
            "email",
            "uploaded_files",
            
            
            "slug",
            "created_at",
            "updated_at",
        ]
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # لعرض تفاصيل المستخدم
        representation['course'] = CourseSerializer(instance.course).data  # لعرض تفاصيل المستخدم
        representation['coupon_course'] = CouponCourseSerializer(instance.coupon_course).data  # لعرض تفاصيل المستخدم
        return representation


# ******************************************************************************
# ==============================================================================
# *** Documents *** #
class DocumentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 

    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.Document
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # لعرض تفاصيل المستخدم
        return representation




# ******************************************************************************
# ==============================================================================
# *** Questions Banks *** #
class ChoiceQuestionInBankSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    # question = serializers.PrimaryKeyRelatedField(queryset=models.SectionCourse.objects.all()) 
    # section = SectionCourseSerializer(many=True, read_only=True)

    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.ChoiceQuestionInBank
        # fields = ['id', 'text', 'is_correct']
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # لعرض تفاصيل المستخدم
        # representation['question'] = QuestionBankSerializer(instance.question).data  # لعرض تفاصيل المستخدم
        return representation
    

class QuestionInBankSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    question_bank = serializers.PrimaryKeyRelatedField(queryset=models.QuestionBank.objects.all()) 
    # question_bank = QuestionBankSerializer(many=True, read_only=True)

    # choices = ChoiceQuestionInBankSerializer(many=True)
    
    class Meta:
        model = models.QuestionInBank
        fields = "__all__"
        # fields = [
        #     'id', 

        #     "user",
        #     "question_bank",

        #     'text', 
        #     'image', 
        #     'image_url', 
        #     # 'display_image', 
        #     'choices',

        #     "slug", 
        #     "created_at",
        #     "updated_at",
        # ]
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # لعرض تفاصيل المستخدم
        representation['question_bank'] = QuestionBankSerializer(instance.question_bank).data  # لعرض تفاصيل المستخدم
        return representation
    

class QuestionInBankDetailSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    question_bank = serializers.PrimaryKeyRelatedField(queryset=models.QuestionBank.objects.all()) 

    choices = ChoiceQuestionInBankSerializer(many=True, source='choices_question_in_bank', read_only=True)
 
    
    class Meta:
        model = models.QuestionInBank
        # fields = ['id', 'text', 'image', 'image_url', 'display_image', 'choices']
        fields = "__all__"
    
    def create(self, validated_data):
        # choices_data = validated_data.pop('choices', [])
        choices_data = validated_data.pop('choices', [])
        question = models.QuestionInBank.objects.create(**validated_data)
        
        for choice_data in choices_data:
            models.ChoiceQuestionInBank.objects.create(question=question, **choice_data)
        # print("\n\n\n\n\n\n\n\n\n\n\n")
        # print("validated_data", validated_data)
        # print("question", question)
        # print("choices_data", choices_data)
        # print("\n\n\n\n\n\n\n\n\n\n\n")
        return question
    
    def update(self, instance, validated_data):
        choices_data = validated_data.pop('choices', None)
        
        # Update question fields
        # instance.text = validated_data.get('text', instance.text)
        
        # instance.image = validated_data.get('image', instance.image)
        # instance.image_url = validated_data.get('image_url', instance.image_url)
        # instance.save()

        # Update question fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update choices if provided
        if choices_data is not None:
            # Delete existing choices
            instance.choices.all().delete()
            
            # Create new choices
            for choice_data in choices_data:
                models.ChoiceQuestionInBank.objects.create(question=instance, **choice_data)
        
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # لعرض تفاصيل المستخدم
        representation['question_bank'] = QuestionBankSerializer(instance.question_bank).data  # لعرض تفاصيل المستخدم
        return representation
    



class QuestionBankSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    section = serializers.PrimaryKeyRelatedField(queryset=models.SectionCourse.objects.all()) 

    question_count = serializers.IntegerField(read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.QuestionBank
        # fields = "__all__"
        fields = [
            'id',

            "user",
            "section",
            
            'title', 
            'description', 
            'image', 
            'image_url', 

            'is_visible', 

            'section_name', 
            'question_count',

            'total_question_in_bank',
            "total_student_result",
            'question_count',
            'display_image', 
            
            "slug", 
            "created_at",
            "updated_at",
        ]
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # لعرض تفاصيل المستخدم
        representation['section'] = SectionCourseSerializer(instance.section).data  # لعرض تفاصيل المستخدم
        return representation



class QuestionBankDetailSerializer(serializers.ModelSerializer):
    questions = QuestionInCourseSerializer(many=True, read_only=True)
    section_name = serializers.CharField(source='section.name', read_only=True)
    
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.QuestionBank 
        fields = "__all__"
        # fields = ['id', 'title', 'description', 'image', 'image_url', 
        #           'display_image', 'section', 'section_name', 'questions']









# ******************************************************************************
# ==============================================================================
# ***   *** #

# class QuestionBankResultSerializer(serializers.Serializer): # QuizResult
#     question_id = serializers.IntegerField()
#     selected_choice_id = serializers.IntegerField(allow_null=True)



# class StudentQuestionBankResultSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
#     question_bank = QuestionBankSerializer(many=True, read_only=True)

#     class Meta:
#         model = models.StudentQuestionBankResult
#         fields = '__all__'
#         # read_only_fields = ('user', 'created_at')
    
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['user'] = UserSerializer(instance.user).data  # لعرض تفاصيل المستخدم
#         return representation


# class StudentQuestionBankAnswerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.StudentQuestionBankAnswer
#         fields = '__all__'
#         extra_kwargs = {
#             'all_choices': {'write_only': True}
#         }








# ******************************************************************************
# ==============================================================================
class StudentQuestionBankResultSerializer(serializers.ModelSerializer):
    """Serializer for Student Question Bank Result (admin view)"""
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    question_bank = serializers.PrimaryKeyRelatedField(queryset=models.QuestionBank.objects.all()) 

    slug = serializers.SlugField(read_only=True)
  
    class Meta:
        model = models.StudentQuestionBankResult
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # لعرض تفاصيل المستخدم
        representation['question_bank'] = QuestionBankSerializer(instance.question_bank).data  # لعرض تفاصيل المستخدم
        return representation






# ******************************************************************************
# ==============================================================================
# *** ContactUs *** #
class ContactUsUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 

    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.ContactUsUser
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # لعرض تفاصيل المستخدم
        return representation





# ******************************************************************************
# ==============================================================================
# *** Review *** #
class ReviewUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) 
    profile = serializers.PrimaryKeyRelatedField(queryset=StudentProfile.objects.all()) 

    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.ReviewUser
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # لعرض تفاصيل المستخدم
        representation['profile'] = StudentProfileSerializer(instance.profile).data  # لعرض تفاصيل المستخدم
        return representation




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