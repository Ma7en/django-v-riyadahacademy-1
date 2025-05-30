# 
import random
import requests
import uuid



# 
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.flatpages.models import FlatPage
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from django.core.files.base import ContentFile



# 
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


# 
from io import BytesIO
from datetime import datetime


# 
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)



# 
from . import models
from . import serializers



# Create your views here.



# ******************************************************************************
# ==============================================================================
# *** Pagination *** #
class StandardResultSetPagination(PageNumberPagination):
    page_size=8
    page_size_query_param='page_size'
    max_page_size = 100






# ******************************************************************************
# ==============================================================================
# *** Category Section *** #
class CategorySectionList(generics.ListCreateAPIView):
    queryset = models.CategorySection.objects.all()
    serializer_class = serializers.CategorySectionSerializer
    pagination_class = StandardResultSetPagination


class CategorySectionPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CategorySection.objects.all()
    serializer_class = serializers.CategorySectionSerializer







# ******************************************************************************
# ==============================================================================
# *** Section Course *** #
class SectionCourseList(generics.ListCreateAPIView):
    queryset = models.SectionCourse.objects.all()
    serializer_class = serializers.SectionCourseSerializer
    pagination_class = StandardResultSetPagination


class SectionCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SectionCourse.objects.all()
    serializer_class = serializers.SectionCourseSerializer





# ******************************************************************************
# ==============================================================================
# *** Course *** #
class CourseList(generics.ListCreateAPIView):
    # queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return models.Course.objects.all()
        else:
            return models.Course.objects.filter(user=user)


class CoursePK(generics.RetrieveUpdateDestroyAPIView):
    # queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
                # هذه السطر يحل مشكلة إنشاء schema
        if getattr(self, 'swagger_fake_view', False):
            return models.Course.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return models.Course.objects.all()
        else:
            return models.Course.objects.filter(user=user)


class CourseListAPI(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        qs = super().get_queryset()
        if 'result' in self.request.GET:
            limit = int(self.request.GET['result'])
            qs = models.Course.objects.all().order_by('-id')[:limit]

        if 'popular' in self.request.GET:
            qs = models.Course.objects.all().order_by('-id')[:limit]

        if 'category' in self.request.GET :
            category = self.request.GET['category']
            category = models.SectionCourse.objects.filter(id=category).first()
            qs = models.Course.objects.filter(category=category)

        if 'skill_name' in self.request.GET and 'teacher' in self.request.GET:
            skill_name = self.request.GET['skill_name']
            teacher = self.request.GET['teacher']
            teacher = models.User.objects.filter(id=teacher).first()
            qs = models.Course.objects.filter(techs__icontains=skill_name,teacher=teacher)

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring']
            qs = models.Course.objects.filter(Q(title__icontains=search)|Q(title__icontains=search))
        
        return qs



class CourseListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.CourseSerializer
    pagination_class = StandardResultSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return models.Course.objects.all()
        return models.Course.objects.filter(user=user)


class CourseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
                # هذه السطر يحل مشكلة إنشاء schema
        if getattr(self, 'swagger_fake_view', False):
            return models.Course.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return models.Course.objects.all()
        return models.Course.objects.filter(user=user)
    

class PublicCourseList(generics.ListAPIView):
    serializer_class = serializers.CourseSerializer
    pagination_class = StandardResultSetPagination
    
    def get_queryset(self):
        queryset = models.Course.objects.filter(is_visible=True)
        
        # # Filter by category
        # category = self.request.query_params.get('category')
        # if category:
        #     queryset = queryset.filter(category__id=category)

        # Filter by section
        section = self.request.query_params.get('section')
        if section:
            queryset = queryset.filter(section__id=section)
        
        # Filter by level
        level = self.request.query_params.get('level')
        if level:
            queryset = queryset.filter(level=level)
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search))
        
        return queryset



# *** Section In Course *** #
class SectionInCourseList(generics.ListCreateAPIView):
    queryset = models.SectionInCourse.objects.all()
    serializer_class = serializers.SectionInCourseSerializer


class SectionInCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SectionInCourse.objects.all()
    serializer_class = serializers.SectionInCourseSerializer


class SectionInCourseListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.SectionInCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return models.SectionInCourse.objects.filter(course__id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_id')
        course = models.Course.objects.get(id=course_id)
        serializer.save(course=course)


class SectionInCourseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.SectionInCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return models.SectionInCourse.objects.filter(course__id=course_id)
    





# *** Lesson In Course *** #
class LessonInCourseList(generics.ListCreateAPIView):
    queryset = models.LessonInCourse.objects.all()
    serializer_class = serializers.LessonInCourseSerializer


class LessonInCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.LessonInCourse.objects.all()
    serializer_class = serializers.LessonInCourseSerializer



class LessonInCourseListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.LessonInCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        section_id = self.kwargs.get('section_id')
        return models.LessonInCourse.objects.filter(section__id=section_id)

    def perform_create(self, serializer):
        section_id = self.kwargs.get('section_id')
        section = models.SectionInCourse.objects.get(id=section_id)
        serializer.save(section=section)


class LessonInCourseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.LessonInCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        section_id = self.kwargs.get('section_id')
        return models.LessonInCourse.objects.filter(section__id=section_id)


class LessonCreateView(generics.CreateAPIView):
    queryset = models.LessonInCourse.objects.all()
    serializer_class = serializers.LessonInCourseSerializer

    def create(self, request, *args, **kwargs):
        section_id = kwargs.get('section_id')
        section = models.SectionInCourse.objects.get(id=section_id)
        
        data = request.data.copy()
        data['section'] = section.id
        
        # Handle video file upload if present
        if 'video_file' in request.FILES:
            data['video_file'] = request.FILES['video_file']
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Handle files and questions if provided
        lesson = serializer.instance
        
        # Process files
        if 'files' in request.FILES:
            files = request.FILES.getlist('files')
            for file in files:
                models.FileInCourse.objects.create(
                    lesson=lesson,
                    name=file.name,
                    file=file,
                    size=file.size,
                    file_type=file.content_type
                )
        
        # Process questions (for assessments)
        if data.get('type') == 'assessment' and 'questions' in data:
            questions_data = data.get('questions', [])
            for question_data in questions_data:
                models.QuestionInCourse.objects.create(
                    lesson=lesson,
                    question_type=question_data.get('question_type'),
                    text=question_data.get('text'),
                    image_url=question_data.get('image_url'),
                    options=question_data.get('options', []),
                    correct_answer=question_data.get('correct_answer', 0)
                )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    





# *** File In Course *** #
class FileInCourseList(generics.ListCreateAPIView):
    queryset = models.FileInCourse.objects.all()
    serializer_class = serializers.FileInCourseSerializer


class FileInCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FileInCourse.objects.all()
    serializer_class = serializers.FileInCourseSerializer


class FileInCourseListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.FileInCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lesson_id = self.kwargs.get('lesson_id')
        return models.FileInCourse.objects.filter(lesson__id=lesson_id)

    def perform_create(self, serializer):
        lesson_id = self.kwargs.get('lesson_id')
        lesson = models.LessonInCourse.objects.get(id=lesson_id)
        serializer.save(lesson=lesson)


class FileInCourseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.FileInCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lesson_id = self.kwargs.get('lesson_id')
        return models.FileInCourse.objects.filter(lesson__id=lesson_id)
    

class FileInCourseCreateView(generics.CreateAPIView):
    queryset = models.FileInCourse.objects.all()
    serializer_class = serializers.FileInCourseSerializer

    def create(self, request, *args, **kwargs):
        lesson_id = kwargs.get('lesson_id')
        lesson = models.LessonInCourse.objects.get(id=lesson_id)
        
        # Handle multiple file uploads
        files = request.FILES.getlist('files')
        created_files = []
        
        for file in files:
            file_data = {
                'lesson': lesson.id,
                'name': file.name,
                'file': file,
                'size': file.size,
                'file_type': file.content_type,
            }
            
            serializer = self.get_serializer(data=file_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            created_files.append(serializer.data)
        
        return Response(created_files, status=status.HTTP_201_CREATED)





# *** Question In Course *** #
class QuestionInCourseList(generics.ListCreateAPIView):
    queryset = models.QuestionInCourse.objects.all()
    serializer_class = serializers.QuestionInCourseSerializer


class QuestionInCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.QuestionInCourse.objects.all()
    serializer_class = serializers.QuestionInCourseSerializer


class QuestionInCourseListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.QuestionInCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lesson_id = self.kwargs.get('lesson_id')
        return models.QuestionInCourse.objects.filter(lesson__id=lesson_id)

    def perform_create(self, serializer):
        lesson_id = self.kwargs.get('lesson_id')
        lesson = models.LessonInCourse.objects.get(id=lesson_id)
        serializer.save(lesson=lesson)


class QuestionInCourseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.QuestionInCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lesson_id = self.kwargs.get('lesson_id')
        return models.QuestionInCourse.objects.filter(lesson__id=lesson_id)


class QuestionCreateView(generics.CreateAPIView):
    queryset = models.QuestionInCourse.objects.all()
    serializer_class = serializers.QuestionInCourseSerializer

    def create(self, request, *args, **kwargs):
        lesson_id = kwargs.get('lesson_id')
        lesson = models.LessonInCourse.objects.get(id=lesson_id)
        
        # Handle multiple questions
        questions_data = request.data if isinstance(request.data, list) else [request.data]
        created_questions = []
        
        for question_data in questions_data:
            question_data['lesson'] = lesson.id
            
            # Handle image file upload if present
            if 'image_file' in request.FILES:
                question_data['image_file'] = request.FILES['image_file']
            
            serializer = self.get_serializer(data=question_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            created_questions.append(serializer.data)
        
        return Response(created_questions, status=status.HTTP_201_CREATED)
    




# class CourseViewSet(viewsets.ModelViewSet):
#     queryset = models.Course.objects.all()
#     serializer_class = serializer.CourseSerializer

# class SectionViewSet(viewsets.ModelViewSet):
#     queryset = models.Section.objects.all()
#     serializer_class = serializer.SectionSerializer

# class ItemViewSet(viewsets.ModelViewSet):
#     queryset = models.Item.objects.all()
#     serializer_class = serializer.ItemSerializer

# class FileViewSet(viewsets.ModelViewSet):
#     queryset = models.File.objects.all()
#     serializer_class = serializer.FileSerializer

# class QuestionViewSet(viewsets.ModelViewSet):
#     queryset = models.Question.objects.all()
#     serializer_class = serializer.QuestionSerializer








# ******************************************************************************
# ==============================================================================
# *** Coupon Course *** #
class CouponCourseList(generics.ListCreateAPIView):
    queryset = models.CouponCourse.objects.all()
    serializer_class = serializers.CouponCourseSerializer
    pagination_class = StandardResultSetPagination


class CouponCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CouponCourse.objects.all()
    serializer_class = serializers.CouponCourseSerializer


class CouponCourseSearch(generics.ListCreateAPIView):
    queryset = models.CouponCourse.objects.all()
    serializer_class = serializers.CouponCourseSerializer
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        if 'searchcoupon' in self.kwargs:
            search = self.kwargs['searchcoupon']
            coupon = models.CouponCourse.objects.get(name=search)
            return coupon








# ******************************************************************************
# ==============================================================================
# *** Course Payment Checkout *** #
class CourseCreateCheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        course = models.Course.objects.get(id=course_id)

        url = f"{settings.HYPERPAY_BASE_URL}/v1/checkouts"
        data = {
            'entityId': settings.HYPERPAY_ENTITY_ID,
            'amount': str(course.price),
            'currency': 'SAR',
            'paymentType': 'DB',
        }
        headers = {
            'Authorization': f"Bearer {settings.HYPERPAY_ACCESS_TOKEN}"
        }
        response = requests.post(url, data=data, headers=headers)
        return Response(response.json())

class CoursePaymentResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        resource_path = request.GET.get('resourcePath')
        course_id = request.GET.get('course_id')

        url = f"{settings.HYPERPAY_BASE_URL}{resource_path}"
        headers = {
            'Authorization': f"Bearer {settings.HYPERPAY_ACCESS_TOKEN}"
        }
        response = requests.get(url, headers=headers)
        result = response.json()

        if result.get("result", {}).get("code") == "000.100.110":  # successful payment
            models.StudentCourseEnrollment.objects.get_or_create(
                user=request.user,
                course_id=course_id,
                defaults={"payment_id": result.get("id")}
            )
            return Response({
                "status": "success", 
                "message": "Enrollment recorded"
                })
        return Response({
            "status": "failed", 
            "message": "Payment not successful"
            })





# ******************************************************************************
# ==============================================================================
# *** Student Enroll Course *** #
class StudentEnrollCourseList(generics.ListCreateAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = serializers.StudentCourseEnrollSerializer
    pagination_class = StandardResultSetPagination


class StudentEnrollCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = serializers.StudentCourseEnrollSerializer


class EnrolledStuentPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = serializers.StudentCourseEnrollSerializer


def fetch_enroll_status(request,student_id,course_id):
    student = models.User.objects.filter(id=student_id).first()
    course = models.Course.objects.filter(id=course_id).first()
    enroll_status = models.StudentCourseEnrollment.objects.filter(course=course,student=student).count()

    if enroll_status:
        return JsonResponse({'bool':True})
    else:
        return JsonResponse({'bool':False})



class EnrolledStuentList(generics.ListCreateAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = serializers.StudentCourseEnrollSerializer

    def get_queryset(self):
        if 'course_id' in self.kwargs:
            course_id = self.kwargs['course_id']
            course = models.Course.objects.get(pk=course_id)
            return models.StudentCourseEnrollment.objects.filter(course=course)
        
        elif 'teacher_id' in self.kwargs:
            teacher_id = self.kwargs['teacher_id']
            teacher = models.User.objects.get(pk=teacher_id)
            return models.StudentCourseEnrollment.objects.filter(course__teacher=teacher).distinct()
        
        elif 'student_id' in self.kwargs:
            student_id = self.kwargs['student_id']
            student = models.User.objects.get(pk=student_id)
            return models.StudentCourseEnrollment.objects.filter(student=student).distinct()
        
        elif 'studentId' in self.kwargs:
            student_id = self.kwargs['student_id']
            student = models.User.objects.get(pk=student_id)
            print(student.interseted_categories)
            queries = [Q(techs__iendwith=value) for value in student.interseted_categories]
            query = queries.pop()
            for item in queries:
                query |= item
            qs = models.Course.objects.filter(query)

        return qs







# ******************************************************************************
# ==============================================================================
# *** Course Rating ***
class CourseRatingList(generics.ListCreateAPIView):
    queryset = models.CourseRating.objects.all()
    serializer_class = serializers.CourseRatingSerializer
    pagination_class = StandardResultSetPagination


class CourseRatingPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CourseRating.objects.all()
    serializer_class = serializers.CourseRatingSerializer




class CourseRatingListAPI(generics.ListCreateAPIView):
    queryset = models.CourseRating.objects.all()
    serializer_class = serializers.CourseRatingSerializer
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        if 'popular' in self.request.GET:
            sql = "SELECT *, AVG(cr.rating) as avg_rating FROM main_courserating as cr INNER JOIN main_course as c ON cr.course_id=c.id GROUP BY c.id ORDER BY avg_rating desc LIMIT 3"
            return models.CourseRating.objects.raw(sql)
        
        if 'all' in self.request.GET:
            sql = "SELECT *, AVG(cr.rating) as avg_rating FROM main_courserating as cr INNER JOIN main_course as c ON cr.course_id=c.id GROUP BY c.id ORDER BY avg_rating desc"
            return models.CourseRating.objects.raw(sql)
        
        return models.CourseRating.objects.filter(course__isnull=False).order_by('-rating')


def fetch_rating_status(request,student_id,course_id):
    student = models.User.objects.filter(id=student_id).first()
    course = models.Course.objects.filter(id=course_id).first()
    rating_status = models.CourseRating.objects.filter(course=course,student=student).count()

    if rating_status:
        return JsonResponse({'bool':True})
    else:
        return JsonResponse({'bool':False})









# ******************************************************************************
# ==============================================================================
# *** Student Favorite Course ***
class StudentFavoriteCourseList(generics.ListCreateAPIView):
    queryset = models.StudentFavoriteCourse.objects.all()
    serializer_class = serializers.StudentFavoriteCourseSerializer
    pagination_class = StandardResultSetPagination


class StudentFavoriteCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.StudentFavoriteCourse.objects.all()
    serializer_class = serializers.StudentFavoriteCourseSerializer




class StudentFavoriteCourseListAPI(generics.ListCreateAPIView):
    queryset = models.StudentFavoriteCourse.objects.all()
    serializer_class = serializers.StudentFavoriteCourseSerializer
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        if 'student_id' in self.kwargs:
            student_id = self.kwargs['student_id']
            student = models.User.objects.get(pk=student_id)
            return models.StudentFavoriteCourse.objects.filter(student=student).distinct()


def remove_favorite_course(request,course_id,student_id):
    student = models.User.objects.filter(id=student_id).first()
    course = models.Course.objects.filter(id=course_id).first()
    favorite_status = models.StudentFavoriteCourse.objects.filter(course=course,student=student).delete()

    if favorite_status:
        return JsonResponse({'bool':True})
    else:
        return JsonResponse({'bool':False})







# ******************************************************************************
# ==============================================================================
# *** Teacher Student Chat ***
class TeacherStudentChatList(generics.ListCreateAPIView):
    queryset = models.TeacherStudentChat.objects.all()
    serializer_class = serializers.TeacherStudentChatSerializer
    pagination_class = StandardResultSetPagination

class TeacherStudentChatPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.TeacherStudentChat.objects.all()
    serializer_class = serializers.TeacherStudentChatSerializer



@csrf_exempt
def TeacherStudentChatBot(request,teacher_id,student_id):
    teacher = models.User.objects.get(id=teacher_id)
    student = models.User.objects.get(id=student_id)
    msg_to = request.POST.get('msg_to')
    msg_from = request.POST.get('msg_from')
    msg_res = models.TeacherStudentChat.objects.create(
        teacher=teacher,
        student=student,
        msg_to=msg_to,
        msg_from=msg_from
    )

    if msg_res:
        return JsonResponse({'bool':True,'msg':'Message sended'})
    else:
        return JsonResponse({'bool':False,'msg':'Message failed'})


class TeacherStudentChatListAPI(generics.ListAPIView):
    queryset = models.TeacherStudentChat.objects.all()
    serializer_class = serializers.TeacherStudentChatSerializer

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        student_id = self.kwargs['student_id']
        teacher = models.User.objects.get(pk=teacher_id)
        student = models.User.objects.get(pk=student_id)
        return models.TeacherStudentChat.objects.filter(teacher=teacher,student=student).exclude(msg_to='')


@csrf_exempt
def GroupTeacherStudentChatBot(request,teacher_id):
    teacher = models.User.objects.get(id=teacher_id)
    msg_to = request.POST.get('msg_to')
    msg_from = request.POST.get('msg_from')
    enrolled_list = models.StudentCourseEnrollment.objects.filter(course__teacher=teacher).distinct()
    
    for enrolled in enrolled_list:
        msg_res = models.TeacherStudentChat.objects.create(
            teacher=teacher,
            student=enrolled.student,
            msg_to=msg_to,
            msg_from=msg_from
        )

    if msg_res:
        return JsonResponse({'bool':True,'msg':'Message sended'})
    else:
        return JsonResponse({'bool':False,'msg':'Message failed'})





# ******************************************************************************
# ==============================================================================
# *** Student Progress Course *** #
class TrackLessonProgressView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def post(self, request, lesson_id):
        try:
            lesson = models.LessonInCourse.objects.get(id=lesson_id)
            completion, created = models.LessonInCourseCompletion.objects.get_or_create(
                user=request.user,
                lesson=lesson
            )
            
            if not completion.is_completed:
                completion.is_completed = True
                completion.completed_at = timezone.now()
                completion.save()
            
            # Update course progress
            course_progress, _ = models.CourseProgress.objects.get_or_create(
                user=request.user,
                course=lesson.section.course
            )
            course_progress.update_progress()
            
            return Response({
                'status': 'success',
                'message': 'Lesson progress updated',
                'progress': course_progress.progress_percentage
            })
        
        except models.LessonInCourse.DoesNotExist:
            return Response({'error': 'Lesson not found'}, status=404)


class GetUserProgressView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        courses_progress = models.CourseProgress.objects.filter(user=request.user)
        serializer = serializers.CourseProgressSerializer(courses_progress, many=True, context={'request': request})
        return Response(serializer.data)




# ******************************************************************************
# ==============================================================================
# *** Student Certificate ***
def student_generate_certificate(request, enrollment_id):
    enrollment = models.StudentCourseEnrollment.objects.get(id=enrollment_id)
    
    # تحقق من أن الطالب قد أكمل الكورس
    # if not enrollment.completed:
    #     return HttpResponse("Course not completed yet", status=400)
    
    # إنشاء PDF في الذاكرة
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    
    # إعداد الصفحة
    width, height = A4
    
    # إضافة خلفية (اختياري)
    # p.drawImage("path/to/certificate_template.jpg", 0, 0, width=width, height=height)
    
    # إضافة محتوى الشهادة
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width/2, height-150, "شهادة إنجاز")
    
    p.setFont("Helvetica", 18)
    p.drawCentredString(width/2, height-200, "تعلن منصة الريادة بأن")
    
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width/2, height-250, f"{enrollment.student.get_full_name()}")
    
    p.setFont("Helvetica", 16)
    p.drawCentredString(width/2, height-300, "قد أكمل بنجاح دورة")
    
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width/2, height-350, f"{enrollment.course.title}")
    
    p.setFont("Helvetica", 14)
    p.drawCentredString(width/2, height-400, f"بتاريخ: {enrollment.completion_date.strftime('%Y-%m-%d')}")
    
    p.setFont("Helvetica", 12)
    p.drawCentredString(width/2, 100, f"رقم الشهادة: {enrollment.certificate_id}")
    
    # حفظ PDF
    p.showPage()
    p.save()
    
    buffer.seek(0)
    
    # إنشاء response
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{enrollment.certificate_id}.pdf"'
    
    return response


class StudentGenerateCertificateView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def post(self, request, course_id):
        try:
            course = models.Course.objects.get(id=course_id)
            user = request.user
            
            # تحقق من إكمال الكورس
            # progress = CourseProgress.objects.filter(user=user, course=course).first()
            # if not progress or progress.progress_percentage < 100:
            #     return Response(
            #         {'error': 'Course not completed yet'}, 
            #         status=status.HTTP_400_BAD_REQUEST
            #     )
            
            # تحقق من وجود شهادة مسبقة
            if models.StudentCertificate.objects.filter(user=user, course=course).exists():
                certificate = models.StudentCertificate.objects.get(user=user, course=course)
                serializer = serializers.StudentCertificateSerializer(certificate)
                return Response(serializer.data)
            
            # إنشاء شهادة جديدة
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter
            
            # تصميم الشهادة
            p.setFont("Helvetica-Bold", 24)
            p.drawCentredString(width/2, height-150, "Certificate of Completion")
            
            p.setFont("Helvetica", 16)
            p.drawCentredString(width/2, height-200, f"This is to certify that")
            
            p.setFont("Helvetica-Bold", 20)
            p.drawCentredString(width/2, height-240, user.get_full_name())
            
            p.setFont("Helvetica", 16)
            p.drawCentredString(width/2, height-280, f"has successfully completed the course")
            
            p.setFont("Helvetica-Bold", 18)
            p.drawCentredString(width/2, height-320, course.title)
            
            p.setFont("Helvetica", 14)
            p.drawCentredString(width/2, height-360, f"Issued on: {datetime.now().strftime('%B %d, %Y')}")
            
            p.setFont("Helvetica", 10)
            p.drawCentredString(width/2, height-400, f"Verification Code: {str(uuid.uuid4().hex)[:16].upper()}")
            
            p.showPage()
            p.save()
            
            # حفظ ملف PDF
            buffer.seek(0)
            pdf_content = ContentFile(buffer.getvalue())
            
            certificate = models.StudentCertificate(
                user=user,
                course=course,
                completion_date=datetime.now()
            )
            certificate.certificate_pdf.save(
                f"certificate_{user.id}_{course.id}.pdf", 
                pdf_content
            )
            certificate.save()
            
            # إنشاء رابط للشهادة
            certificate_url = request.build_absolute_uri(certificate.certificate_pdf.url)
            certificate.certificate_url = certificate_url
            certificate.save()
            
            serializer = serializers.StudentCertificateSerializer(certificate)
            return Response(serializer.data)
            
        except models.Course.DoesNotExist:
            return Response(
                {'error': 'Course not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class StudentCertificatesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        certificates = models.StudentCertificate.objects.filter(user=request.user)
        serializer = serializers.StudentCertificateSerializer(certificates, many=True)
        return Response(serializer.data)


class StudentVerifyCertificateView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, verification_code):
        try:
            certificate = models.StudentCertificate.objects.get(verification_code=verification_code)
            serializer = serializers.StudentCertificateSerializer(certificate)
            return Response(serializer.data)
        except models.StudentCertificate.DoesNotExist:
            return Response(
                {
                    'error': 'Invalid verification code'
                }, 
                status=status.HTTP_404_NOT_FOUND
            )
        


# ******************************************************************************
# ==============================================================================
# *** Question Bank ***
class QuestionBankList(generics.ListCreateAPIView):
    # queryset = models.QuestionBank.objects.all()
    serializer_class = serializers.QuestionBankListSerializer
    pagination_class = StandardResultSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return models.QuestionBank.objects.all()
        else:
            return models.QuestionBank.objects.filter(user=user)

class QuestionBankPK(generics.RetrieveUpdateDestroyAPIView):
    # queryset = models.QuestionBank.objects.all()
    serializer_class = serializers.QuestionBankListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # هذه السطر يحل مشكلة إنشاء schema
        if getattr(self, 'swagger_fake_view', False):
            return models.QuestionBank.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return models.QuestionBank.objects.all()
        else:
            return models.QuestionBank.objects.filter(user=user)



class QuestionBankViewSet(viewsets.ModelViewSet):
    queryset = models.QuestionBank.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.QuestionBankDetailSerializer
        return serializers.QuestionBankListSerializer
    
    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        """Get all questions for a question bank"""
        question_bank = self.get_object()
        questions = question_bank.questions.all()
        serializer = serializers.QuestionBankListSerializer(questions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def quiz(self, request, pk=None):
        """Get randomized questions for quiz taking"""
        question_bank = self.get_object()
        questions = list(question_bank.questions.all())
        
        # Randomize questions
        random.shuffle(questions)
        
        # Serialize questions but exclude is_correct from choices
        serialized_questions = []
        for question in questions:
            question_data = serializers.QuestionBankListSerializer(question).data
            
            # Remove is_correct field from choices
            for choice in question_data['choices']:
                if 'is_correct' in choice:
                    del choice['is_correct']
            
            serialized_questions.append(question_data)
        
        return Response(serialized_questions)


class QuestionInBankViewSet(viewsets.ModelViewSet):
    queryset = models.QuestionInBank.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return serializers.QuestionInBankDetailSerializer
        return serializers.QuestionInBankSerializer
    
    def get_queryset(self):
        queryset = models.QuestionInBank.objects.all()
        question_bank_id = self.request.query_params.get('question_bank')
        
        if question_bank_id:
            queryset = queryset.filter(question_bank_id=question_bank_id)
        
        return queryset


# old code 
# class QuestionBankResultView(APIView):
#     def post(self, request, question_bank_id):
#         """Calculate quiz results"""
#         # Get the question bank
#         question_bank = get_object_or_404(models.QuestionBank, pk=question_bank_id)
        
#         # Validate the request data
#         serializer = serializer.QuestionBankResultSerializer(data=request.data, many=True)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         # Process the results
#         answers = serializer.validated_data
#         total_questions = len(answers)
#         correct_answers = 0
#         results = []
        
#         for answer in answers:
#             question_id = answer['question_id']
#             selected_choice_id = answer['selected_choice_id']
            
#             # Get the question and its correct choice
#             question = get_object_or_404(models.QuestionInBank, pk=question_id)
#             correct_choice = question.choices.filter(is_correct=True).first()
            
#             # Check if the answer is correct
#             is_correct = correct_choice.id == selected_choice_id if correct_choice else False
#             if is_correct:
#                 correct_answers += 1
            
#             # Add to results
#             results.append({
#                 'question_id': question_id,
#                 'question_text': question.text,
#                 'selected_choice_id': selected_choice_id,
#                 'correct_choice_id': correct_choice.id if correct_choice else None,
#                 'is_correct': is_correct
#             })
        
#         # Calculate percentage
#         percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
#         return Response({
#             'total_questions': total_questions,
#             'correct_answers': correct_answers,
#             'percentage': round(percentage, 2),
#             'results': results
#         })


# 
class QuestionBankResultView(APIView):
    def post(self, request, question_bank_id):
        """Calculate quiz results"""
        # Get the question bank
        question_bank = get_object_or_404(models.QuestionBank, pk=question_bank_id)
        
        # Get all questions for this bank
        all_questions = models.QuestionInBank.objects.filter(question_bank_id=question_bank_id)
        
        # Validate the request data
        serializer = serializers.QuestionBankResultSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Process the results
        submitted_answers = {answer['question_id']: answer['selected_choice_id'] for answer in serializer.validated_data}
        total_questions = all_questions.count()
        correct_answers = 0
        results = []
        
        for question in all_questions:
            question_id = question.id
            selected_choice_id = submitted_answers.get(question_id)
            
            # Get the correct choice
            correct_choice = question.choices.filter(is_correct=True).first()
            
            # Check if the answer is correct (only if answered)
            is_answered = question_id in submitted_answers
            is_correct = False
            
            if is_answered and correct_choice:
                is_correct = correct_choice.id == selected_choice_id
                if is_correct:
                    correct_answers += 1
            
            # Add to results
            results.append({
                'question_id': question_id,
                'question_text': question.text,
                'is_answered': is_answered,
                'selected_choice_id': selected_choice_id,
                'correct_choice_id': correct_choice.id if correct_choice else None,
                'is_correct': is_correct,
                'choices': [
                    {
                        'id': choice.id,
                        'text': choice.text,
                        'is_correct': choice.is_correct
                    }
                    for choice in question.choices.all()
                ]
            })
        
        # Calculate percentage
        percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        return Response({
            'total_questions': total_questions,
            'answered_questions': len(submitted_answers),
            'correct_answers': correct_answers,
            'percentage': round(percentage, 2),
            'results': results
        })


# 
class StudentQuestionBankResultSaveView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, question_bank_id):
        question_bank = get_object_or_404(models.QuestionBank, pk=question_bank_id)
        
        result_data = {
            'user': request.user.id,
            'question_bank': question_bank.id,
            'answered_questions': request.data.get('answered_questions'),
            'correct_answers': request.data.get('correct_answers'),
            'percentage': request.data.get('percentage'),
            'total_questions': request.data.get('total_questions'),
        }
        
        result_serializer = serializers.StudentQuestionBankResultSerializer(data=result_data)
        if not result_serializer.is_valid():
            return Response(result_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        quiz_result = result_serializer.save()
        
        answers_data = request.data.get('results', [])
        for answer_data in answers_data:
            selected_choice = next(
                (c for c in answer_data.get('choices', []) if c['id'] == answer_data.get('selected_choice_id')),
                None
            )
            correct_choice = next(
                (c for c in answer_data.get('choices', []) if c.get('is_correct', False)),
                None
            )
            
            answer_data['quiz_result'] = quiz_result.id
            answer_data['selected_choice_text'] = selected_choice['text'] if selected_choice else None
            answer_data['correct_choice_text'] = correct_choice['text'] if correct_choice else None
            answer_data['all_choices'] = answer_data.get('choices', [])
            
            answer_serializer = serializers.StudentQuestionBankAnswerSerializer(data=answer_data)
            if answer_serializer.is_valid():
                answer_serializer.save()
        
        return Response({
            'status': 'success',
            'result_id': quiz_result.id
        }, status=status.HTTP_201_CREATED)
    




# ******************************************************************************
# ==============================================================================
# ***  ***







# ******************************************************************************
# ==============================================================================
# *** ContactUs ***
# (List of contact us -> [GET, POST])
class ContactUsListAPIView(generics.ListCreateAPIView):
    # queryset = models.ContactUsUser.objects.all()
    serializer_class = serializers.ContactUsUserSerializer
    pagination_class = StandardResultSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            return models.ContactUsUser.objects.filter(user=user)
        else:
            return models.ContactUsUser.objects.all()


# (List of contact us -> [GET, POST, PUT, DELETE])
class ContactUsPKAPIView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = models.ContactUsUser.objects.all()
    serializer_class = serializers.ContactUsUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # هذه السطر يمنع المشكلة أثناء إنشاء schema لوثائق API
        if getattr(self, 'swagger_fake_view', False):
            return models.ReviewUser.objects.none()
        
        user = self.request.user
        if user.is_student:
            return models.ContactUsUser.objects.filter(user=user)
        else:
            return models.ContactUsUser.objects.all()







# ******************************************************************************
# ==============================================================================
# *** Review ***
# (List of review -> [GET, POST])
class ReviewUserListAPIView(generics.ListCreateAPIView):
    # queryset = models.ReviewUser.objects.all()
    serializer_class = serializers.ReviewUserSerializer
    pagination_class = StandardResultSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            return models.ReviewUser.objects.filter(user=user)
        else:
            return models.ReviewUser.objects.all()


# (List of review -> [GET, POST, PUT, DELETE])
class ReviewUserPKAPIView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = models.ReviewUser.objects.all()
    serializer_class = serializers.ReviewUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # هذه السطر يمنع المشكلة أثناء إنشاء schema لوثائق API
        if getattr(self, 'swagger_fake_view', False):
            return models.ReviewUser.objects.none()
        
        user = self.request.user
        if user.is_student:
            return models.ReviewUser.objects.filter(user=user)
        else:
            return models.ReviewUser.objects.all()
        




# ******************************************************************************
# ==============================================================================
# ***  ***
# # class CategoryListView(generics.ListCreateAPIView):
# #     queryset = models.Category.objects.all()
# #     serializer_class = serializer.CategorySerializer
# #     lookup_field = "pk"

# #     def get_object(self):
# #         pk = self.kwargs.get("pk")
# #         category = self.queryset.get(pk=pk)
# #         category.view += 1
# #         category.save()
# #         return category

# class CategoryListView(generics.ListCreateAPIView):
#     queryset = models.Category.objects.all()
#     serializer_class = serializer.CategorySerializer

# class CategoryPkAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Category.objects.all()
#     serializer_class = serializer.CategorySerializer

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.view += 1  # زيادة عدد المشاهدات
#         instance.save()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         category = models.Category.objects.get(id=pk)
        
#         # # التحقق مما إذا كان المستخدم قد أعجب بالمقالة مسبقًا
#         if request.user in category.likes.all():
#             category.likes.remove(request.user)  # إزالة الإعجاب إذا كان موجودًا
#             print("\n\n\n\n")
#             print("->", category)
#             print("\n\n\n\n")
#             message = "category unliked!"
#         else:
#             print("\n\n\n\n")
#             print("--->",request.user)
#             print("\n\n\n\n")
#             # category.likes.add(request.user)  # إضافة إعجاب
#             # message = "category liked!"
#             # # إرسال إشعار إلى المستخدم صاحب المقالة
#             # models.Notification.objects.create(
#             #     user=category.user,  # المستخدم صاحب المقالة
#             #     message=f"{request.user.username} liked your category: {category.title}",
#             #     notification_type='like_category',
#             #     category=category,
#             # )
        
#         return Response()
#         # return Response({"message": message, "likes_count": category.likes.count()})

# class PostListView(generics.ListCreateAPIView):
#     queryset = models.Post.objects.all()
#     serializer_class = serializer.PostSerializer

# class PostPkAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Post.objects.all()
#     serializer_class = serializer.PostSerializer

# class CommentListView(generics.ListCreateAPIView):
#     queryset = models.Comment.objects.all()
#     serializer_class = serializer.CommentSerializer
# class CommentPKAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Comment.objects.all()
#     serializer_class = serializer.CommentSerializer

# class ReplyListView(generics.ListCreateAPIView):
#     queryset = models.Reply.objects.all()
#     serializer_class = serializer.ReplySerializer
# class ReplyPKAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Reply.objects.all()
#     serializer_class = serializer.ReplySerializer

# class NotificationListView(generics.ListCreateAPIView):
#     queryset = models.Notification.objects.all()
#     serializer_class = serializer.NotificationSerializer
# class NotificationPKAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Notification.objects.all()
#     serializer_class = serializer.NotificationSerializer

# class ReportListView(generics.ListCreateAPIView):
#     queryset = models.Report.objects.all()
#     serializer_class = serializer.ReportSerializer
# class ReportPKAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Report.objects.all()
#     serializer_class = serializer.ReportSerializer












# ******************************************************************************
# ==============================================================================
# ***  ***
