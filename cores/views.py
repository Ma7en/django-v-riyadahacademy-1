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
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F

# 
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors



# 
from io import BytesIO
from datetime import datetime




# 
from rest_framework import generics, filters
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
from accounts.serializers import *




# 
from . import models
from . import serializers





# Create your views here.



# ******************************************************************************
# ==============================================================================
# *** Pagination *** #
class StandardResultSetPagination(PageNumberPagination):
    page_size=9
    page_size_query_param='page_size'
    max_page_size = 100


class Space(generics.ListCreateAPIView):
    pass




# ******************************************************************************
# ==============================================================================
# *** Startapp ***
class StartappList(generics.ListCreateAPIView):
    queryset = models.Startapp.objects.all()
    serializer_class = serializers.StartappSerializer
    pagination_class = StandardResultSetPagination
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]


class StartappListAdmin(generics.ListCreateAPIView):
    queryset = models.Startapp.objects.all()
    serializer_class = serializers.StartappSerializer
    permission_classes = [AllowAny]


class StartappListApp(generics.ListCreateAPIView):
    queryset = models.Startapp.objects.filter(is_visible=True)
    serializer_class = serializers.StartappSerializer
    # pagination_class = StandardResultSetPagination
    permission_classes = [AllowAny]

        

class StartappResultList(generics.ListCreateAPIView):
    queryset = models.Startapp.objects.all()
    serializer_class = serializers.StartappSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if 'result' in self.request.GET:
            try:
                limit = int(self.request.GET['result'])
                qs = qs.order_by('-id').filter(is_visible=True)[:limit]
            except ValueError:
                # Handle the case where 'result' is not an integer
                pass
        return qs


class StartappPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Startapp.objects.all()
    serializer_class = serializers.StartappSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]


class StartappSearchList(generics.ListCreateAPIView):
    queryset = models.Startapp.objects.all()
    serializer_class = serializers.StartappSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring'] 
            qs = qs.filter(
                Q(title__icontains=search)
                |Q(description__icontains=search)
                )
        return qs






# ******************************************************************************
# ==============================================================================
# *** Category Section *** #
class CategorySectionList(generics.ListCreateAPIView):
    queryset = models.CategorySection.objects.all()
    serializer_class = serializers.CategorySectionSerializer
    pagination_class = StandardResultSetPagination
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]


class CategorySectionListAdmin(generics.ListCreateAPIView):
    queryset = models.CategorySection.objects.all()
    serializer_class = serializers.CategorySectionSerializer
    permission_classes = [AllowAny]


class CategorySectionListApp(generics.ListCreateAPIView):
    queryset = models.CategorySection.objects.filter(is_visible=True)
    serializer_class = serializers.CategorySectionSerializer
    # pagination_class = StandardResultSetPagination
    permission_classes = [AllowAny]


class CategorySectionListAppOrdered(generics.ListCreateAPIView):
    queryset = models.CategorySection.objects.filter(is_visible=True).order_by('created_at')
    serializer_class = serializers.CategorySectionSerializer
    # pagination_class = StandardResultSetPagination
    permission_classes = [AllowAny]
        

class CategorySectionResultList(generics.ListCreateAPIView):
    queryset = models.CategorySection.objects.all()
    serializer_class = serializers.CategorySectionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if 'result' in self.request.GET:
            try:
                limit = int(self.request.GET['result'])
                qs = qs.order_by('-id').filter(is_visible=True)[:limit]
            except ValueError:
                # Handle the case where 'result' is not an integer
                pass
        return qs


class CategorySectionPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CategorySection.objects.all()
    serializer_class = serializers.CategorySectionSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]


class CategorySectionSearchList(generics.ListCreateAPIView):
    queryset = models.CategorySection.objects.all()
    serializer_class = serializers.CategorySectionSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring'] 
            qs = qs.filter(
                Q(title__icontains=search)
                |Q(description__icontains=search)
                )
        return qs





# ******************************************************************************
# ==============================================================================
# *** Section Course *** #
class SectionCourseList(generics.ListCreateAPIView):
    queryset = models.SectionCourse.objects.all()
    serializer_class = serializers.SectionCourseSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]


class SectionCourseListApp(generics.ListCreateAPIView):
    queryset = models.SectionCourse.objects.filter(is_visible=True)
    serializer_class = serializers.SectionCourseSerializer
    permission_classes = [AllowAny]
    # pagination_class = StandardResultSetPagination



class SectionCourseListAdmin(generics.ListCreateAPIView):
    queryset = models.SectionCourse.objects.all()
    serializer_class = serializers.SectionCourseSerializer
    permission_classes = [IsAuthenticated]

        

class SectionCourseResultList(generics.ListCreateAPIView):
    queryset = models.SectionCourse.objects.all()
    serializer_class = serializers.SectionCourseSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if 'result' in self.request.GET:
            try:
                limit = int(self.request.GET['result'])
                qs = qs.order_by('-id').filter(is_visible=True)[:limit]
            except ValueError:
                # Handle the case where 'result' is not an integer
                pass
        return qs



class SectionCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SectionCourse.objects.all()
    serializer_class = serializers.SectionCourseSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]



class SectionCourseSearchList(generics.ListCreateAPIView):
    queryset = models.SectionCourse.objects.all()
    serializer_class = serializers.SectionCourseSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring'] 
            qs = qs.filter(
                Q(title__icontains=search)
                |Q(description__icontains=search)
                |Q(grade__icontains=search)
                )
        return qs




# ******************************************************************************
# ==============================================================================
# *** Section Course *** #
class SectionCourseCategoriesList(generics.ListCreateAPIView):
    queryset = models.SectionCourse.objects.all()
    serializer_class = serializers.SectionCourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_visible']
    search_fields = ['title', 'description', 'grade']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']



class SectionCourseCategoryList(generics.ListCreateAPIView):
    queryset = models.SectionCourse.objects.all()
    serializer_class = serializers.SectionCourseSerializer
    # pagination_class = StandardResultSetPagination
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.kwargs["pk"]
        category = models.CategorySection.objects.get(id=category_id)
        return models.SectionCourse.objects.filter(category=category)




# ******************************************************************************
# ==============================================================================
# *** Course *** #
class CourseList(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    pagination_class = StandardResultSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return models.Course.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return models.Course.objects.all()
        else:
            return models.Course.objects.filter(user=user)


class CourseNotAllList(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseNotAllSerializer
    pagination_class = StandardResultSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return models.Course.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return models.Course.objects.all()
        else:
            return models.Course.objects.filter(user=user)



class CourseListApp(generics.ListCreateAPIView):
    queryset = models.Course.objects.filter(is_visible=True)
    serializer_class = serializers.CourseSerializer
    permission_classes = [AllowAny]
    # pagination_class = StandardResultSetPagination


class CourseNotAllListApp(generics.ListCreateAPIView):
    queryset = models.Course.objects.filter(is_visible=True)
    serializer_class = serializers.CourseNotAllSerializer
    permission_classes = [AllowAny]
    # pagination_class = StandardResultSetPagination


class CourseListAdmin(generics.ListCreateAPIView):
    queryset = models.Course.objects.filter(is_visible=True)
    serializer_class = serializers.CourseSerializer
    permission_classes = [IsAuthenticated]
    # pagination_class = StandardResultSetPagination

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return models.Course.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return models.Course.objects.all()
        else:
            return models.Course.objects.filter(user=user)


class CourseNotAllListAdmin(generics.ListAPIView):
    queryset = models.Course.objects.filter(is_visible=True)
    serializer_class = serializers.CourseNotAllSerializer
    permission_classes = [IsAuthenticated]
    # pagination_class = StandardResultSetPagination

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return models.Course.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return models.Course.objects.all()
        else:
            return models.Course.objects.filter(user=user)

        

class CourseResultList(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if 'result' in self.request.GET:
            try:
                limit = int(self.request.GET['result'])
                qs = qs.order_by('-id').filter(is_visible=True)[:limit]
            except ValueError:
                # Handle the case where 'result' is not an integer
                pass
        return qs
        

class CourseNotAllResultList(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseNotAllSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if 'result' in self.request.GET:
            try:
                limit = int(self.request.GET['result'])
                qs = qs.order_by('-id').filter(is_visible=True)[:limit]
            except ValueError:
                # Handle the case where 'result' is not an integer
                pass
        return qs



class CoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     # هذه السطر يحل مشكلة إنشاء schema
    #     if getattr(self, 'swagger_fake_view', False):
    #         return models.Course.objects.none()
        
    #     user = self.request.user
    #     if user.is_superuser:
    #         return models.Course.objects.all()
    #     else:
    #         return models.Course.objects.filter(user=user)



class CourseAndSectionInCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseAndSectionInCourseSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     # هذه السطر يحل مشكلة إنشاء schema
    #     if getattr(self, 'swagger_fake_view', False):
    #         return models.Course.objects.none()
        
    #     user = self.request.user
    #     if user.is_superuser:
    #         return models.Course.objects.all()
    #     else:
    #         return models.Course.objects.filter(user=user)






class CourseDetailAll(generics.RetrieveAPIView):
    """
    API View لعرض تفاصيل الكورس باستخدام الـ PK
    """
    queryset = models.Course.objects.all()  # كل الكورسات
    serializer_class = serializers.CourseSerializer  # السيريالايزر الذي نستخدمه
    lookup_field = 'pk'  # البحث بالـ PK (هذا هو الافتراضي، يمكن حذفه إذا أردت)



class CourseNotAllDetailAll(generics.RetrieveAPIView):
    """
    API View لعرض تفاصيل الكورس باستخدام الـ PK
    """
    queryset = models.Course.objects.all()  # كل الكورسات
    serializer_class = serializers.CourseNotAllSerializer  # السيريالايزر الذي نستخدمه
    lookup_field = 'pk'  # البحث بالـ PK (هذا هو الافتراضي، يمكن حذفه إذا أردت)



class CourseListAPI(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        if 'result' in self.request.GET:
            limit = int(self.request.GET['result'])
            qs = models.Course.objects.all().order_by('-id')[:limit]

        if 'popular' in self.request.GET:
            qs = models.Course.objects.all().order_by('-id')#[:limit]

        if 'category' in self.request.GET :
            category = self.request.GET['category']
            category = models.SectionCourse.objects.filter(id=category).first()
            qs = models.Course.objects.filter(category=category)

        if 'skill_name' in self.request.GET and 'teacher' in self.request.GET:
            skill_name = self.request.GET['skill_name']
            teacher = self.request.GET['teacher']
            teacher = models.User.objects.filter(id=teacher).first()
            qs = models.Course.objects.filter(techs__icontains=skill_name, teacher=teacher)

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring']
            qs = qs.filter(
                Q(level__icontains=search)
                |Q(title__icontains=search)
                |Q(description__icontains=search)
                |Q(duration__icontains=search)
                |Q(price__icontains=search)
                |Q(discount__icontains=search)
                |Q(rating__icontains=search)
                |Q(language__icontains=search)
                |Q(tag__icontains=search)
                |Q(techs__icontains=search)
                |Q(features__icontains=search)
                |Q(requirements__icontains=search)
                |Q(target_audience__icontains=search)
                )
        
        return qs





class CourseListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.CourseSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return models.Course.objects.all()
        return models.Course.objects.filter(user=user)


class CourseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CourseSerializer
    # permission_classes = [IsAuthenticated]

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
    # permission_classes = [IsAuthenticated]

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



class CoursesSearchList(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring'] 
            qs = qs.filter(
                Q(title__icontains=search)
                |Q(description__icontains=search)
                |Q(level__icontains=search)
                |Q(duration__icontains=search)
                |Q(price__icontains=search)
                |Q(duration__icontains=search)
                |Q(language__icontains=search)
                )
        return qs
    






class CourseSectionCourseList(generics.ListCreateAPIView):
    queryset = models.SectionCourse.objects.all()
    serializer_class = serializers.CourseSerializer
    # pagination_class = StandardResultSetPagination
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        section_id = self.kwargs["pk"]
        section = models.SectionCourse.objects.get(id=section_id)
        return models.Course.objects.filter(section=section)




# ******************************************************************************
# ==============================================================================
# *** Section In Course *** #
class SectionInCourseList(generics.ListCreateAPIView):
    queryset = models.SectionInCourse.objects.all()
    serializer_class = serializers.SectionInCourseSerializer


class SectionInCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SectionInCourse.objects.all()
    serializer_class = serializers.SectionInCourseSerializer


class SectionInCourseListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.SectionInCourseSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return models.SectionInCourse.objects.filter(course__id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_id')
        course = models.Course.objects.get(id=course_id)
        serializer.save(course=course)


class SectionInCourseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.SectionInCourseSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return models.SectionInCourse.objects.filter(course__id=course_id)
    








# ******************************************************************************
# ==============================================================================
# *** Lesson In Course *** #
class LessonInCourseList(generics.ListCreateAPIView):
    queryset = models.LessonInCourse.objects.all()
    serializer_class = serializers.LessonInCourseSerializer


class LessonInCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.LessonInCourse.objects.all()
    serializer_class = serializers.LessonInCourseSerializer



class LessonInCourseListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.LessonInCourseSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        section_id = self.kwargs.get('section_id')
        return models.LessonInCourse.objects.filter(section__id=section_id)

    def perform_create(self, serializer):
        section_id = self.kwargs.get('section_id')
        section = models.SectionInCourse.objects.get(id=section_id)
        serializer.save(section=section)


class LessonInCourseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.LessonInCourseSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        section_id = self.kwargs.get('section_id')
        return models.LessonInCourse.objects.filter(section__id=section_id)


class LessonInCourseCreateView(generics.CreateAPIView):
    queryset = models.LessonInCourse.objects.all()
    serializer_class = serializers.LessonInCourseSerializer
    permission_classes = [AllowAny]

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
        if 'uploaded_files' in request.FILES:
            files = request.FILES.getlist('uploaded_files')
            for file in files:
                models.FileInCourse.objects.create(
                    lesson=lesson,
                    name=file.name,
                    file=file,
                    size=file.size,
                    file_type=file.type
                )
        
        # Process questions (for assessments)
        if data.get('type') == 'assessment' and 'questions' in data:
            questions_data = data.get('questions', [])
            print("\n\n\n\n\n\n")
            print("questions_data", questions_data)
            print("\n\n\n\n\n\n")
            for question_data in questions_data:
                print("\n\n\n\n\n\n")
                print("question_data", question_data)
                print("\n\n\n\n\n\n")
                models.QuestionInCourse.objects.create(
                    lesson=lesson,
                    text=question_data.get('text'),
                    question_type=question_data.get('question_type'),
                    image_url=question_data.get('image_url'),
                    choices=question_data.get('choices', []),
                    correct_answer=question_data.get('correct_answer', 0)
                )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    








# ******************************************************************************
# ==============================================================================
# *** File In Course *** #
class FileInCourseList(generics.ListCreateAPIView):
    queryset = models.FileInCourse.objects.all()
    serializer_class = serializers.FileInCourseSerializer


class FileInCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FileInCourse.objects.all()
    serializer_class = serializers.FileInCourseSerializer


class FileInCourseListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.FileInCourseSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lesson_id = self.kwargs.get('lesson_id')
        return models.FileInCourse.objects.filter(lesson__id=lesson_id)

    def perform_create(self, serializer):
        lesson_id = self.kwargs.get('lesson_id')
        lesson = models.LessonInCourse.objects.get(id=lesson_id)
        serializer.save(lesson=lesson)


class FileInCourseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.FileInCourseSerializer
    # permission_classes = [IsAuthenticated]

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








# ******************************************************************************
# ==============================================================================
# *** Question In Course *** #
class QuestionInCourseList(generics.ListCreateAPIView):
    queryset = models.QuestionInCourse.objects.all()
    serializer_class = serializers.QuestionInCourseSerializer


class QuestionInCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.QuestionInCourse.objects.all()
    serializer_class = serializers.QuestionInCourseSerializer


class QuestionInCourseListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.QuestionInCourseSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lesson_id = self.kwargs.get('lesson_id')
        return models.QuestionInCourse.objects.filter(lesson__id=lesson_id)

    def perform_create(self, serializer):
        lesson_id = self.kwargs.get('lesson_id')
        lesson = models.LessonInCourse.objects.get(id=lesson_id)
        serializer.save(lesson=lesson)


class QuestionInCourseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.QuestionInCourseSerializer
    # permission_classes = [IsAuthenticated]

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
    # permission_classes = [IsAuthenticated]


class CouponCourseListApp(generics.ListCreateAPIView):
    queryset = models.CouponCourse.objects.filter(is_visible=True)
    serializer_class = serializers.CouponCourseSerializer
    permission_classes = [AllowAny]


class CouponCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CouponCourse.objects.all()
    serializer_class = serializers.CouponCourseSerializer
    # permission_classes = [IsAuthenticated]


class CouponCourseSearch(generics.ListCreateAPIView):
    queryset = models.CouponCourse.objects.all()
    serializer_class = serializers.CouponCourseSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring']
            # coupon = models.CouponCourse.objects.get(name=search)
            qs = qs.filter(
                Q(name__icontains=search)
                |Q(discount__icontains=search)
                )
        return qs


class CouponCourseSearchApp(generics.ListCreateAPIView):
    queryset = models.CouponCourse.objects.all()
    serializer_class = serializers.CouponCourseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring']
            qs = qs.filter(is_visible=True).filter(
                Q(name__iexact=search)
            )
        return qs



class CouponCourseSearchAppUsage(generics.ListCreateAPIView):
    queryset = models.CouponCourse.objects.all()
    serializer_class = serializers.CouponCourseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        # Filter for visible coupons and where current_usage is less than usage_limit
        qs = qs.filter(is_visible=True, current_usage__lt=F('usage_limit'))
        
        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring']
            qs = qs.filter(
                Q(name__iexact=search)
            )
        return qs



class CouponCourseIncrementUsageView(generics.UpdateAPIView):
    queryset = models.CouponCourse.objects.all()
    serializer_class = serializers.CouponCourseSerializer
    permission_classes = [AllowAny]
    lookup_field = 'name' # Use coupon name to lookup the coupon

    def update(self, request, *args, **kwargs):
        coupon = self.get_object()
        
        if not coupon.is_valid():
            return Response(
                {'detail': 'Coupon is not valid or has reached its usage limit.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if coupon.decrement_usage():
            serializer = self.get_serializer(coupon)
            return Response(serializer.data)
        else:
            return Response(
                {'detail': 'Failed to increment coupon usage.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class ApplyCouponCourseView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        coupon_name = request.data.get('coupon_name')

        if not coupon_name:
            return Response({
            'detail'
            : 
            'Coupon name is required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            coupon = get_object_or_404(models.CouponCourse, name__iexact=coupon_name)

        except:
            return Response({
            'detail'
            : 
            'Coupon not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        if not coupon.is_valid():
            return Response({
            'detail'
            : 
            'Coupon is not valid or has reached its usage limit.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if coupon.decrement_usage():
            serializer = serializers.CouponCourseSerializer(coupon)
            return Response({
                'detail'
                : 
                'Coupon applied successfully.', 
                'coupon'
                : serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({
                'detail'
                : 
                'Failed to apply coupon.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# ******************************************************************************
# ==============================================================================
# *** Course Payment Checkout *** #
class CourseCreateCheckoutView(APIView):
    # permission_classes = [IsAuthenticated]

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
            # 'Authorization': f"Bearer {settings.HYPERPAY_ACCESS_TOKEN}"
        }
        response = requests.post(url, data=data, headers=headers)
        return Response(response.json())


class CoursePaymentResultView(APIView):
    # permission_classes = [IsAuthenticated]

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
    # permission_classes = [IsAuthenticated]


class StudentEnrollCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = serializers.StudentCourseEnrollSerializer
    # permission_classes = [IsAuthenticated]


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

# class FetchEnrollStatusView(generics.RetrieveAPIView):
class FetchEnrollStatusView(APIView):
    # pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get(self, request, student_id, course_id):
        student = models.User.objects.filter(id=student_id).first()
        course = models.Course.objects.filter(id=course_id).first()
        enroll_status = models.StudentCourseEnrollment.objects.filter(course=course, student=student).exists()
        return Response({'bool': enroll_status})


# class EnrolledStuentList(generics.ListCreateAPIView):
#     queryset = models.StudentCourseEnrollment.objects.all()
#     serializer_class = serializers.StudentCourseEnrollSerializer
#     pagination_class = StandardResultSetPagination
#     permission_classes = [AllowAny]
#     # permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         qs = ""
#         if 'course_id' in self.kwargs:
#             course_id = self.kwargs['course_id']
#             # course = models.Course.objects.get(pk=course_id)
#             return models.StudentCourseEnrollment.objects.filter(course=course_id)
        
#         # elif 'teacher_id' in self.kwargs:
#         #     teacher_id = self.kwargs['teacher_id']
#         #     teacher = models.User.objects.get(pk=teacher_id)
#         #     return models.StudentCourseEnrollment.objects.filter(course__teacher=teacher).distinct()
        
#         # elif 'student_id' in self.kwargs:
#         #     student_id = self.kwargs['student_id']
#         #     student = models.User.objects.get(pk=student_id)
#         #     return models.StudentCourseEnrollment.objects.filter(student=student).distinct()
        
#         # elif 'studentId' in self.kwargs:
#         #     student_id = self.kwargs['student_id']
#         #     student = models.User.objects.get(pk=student_id)
#         #     print(student.interseted_categories)
#         #     queries = [Q(techs__iendwith=value) for value in student.interseted_categories]
#         #     query = queries.pop()
#         #     for item in queries:
#         #         query |= item
#         #     qs = models.Course.objects.filter(query)

#         # return qs


#-
class EnrolledStuentCourseList(generics.ListCreateAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = serializers.StudentCourseEnrollSerializer
    pagination_class = StandardResultSetPagination
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = ""
        if 'course_id' in self.kwargs:
            course_id = self.kwargs['course_id']
            # course = models.Course.objects.get(pk=course_id)
            return models.StudentCourseEnrollment.objects.filter(course=course_id)
        

class EnrolledAllStuentList(generics.ListCreateAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = serializers.StudentCourseEnrollSerializer
    pagination_class = StandardResultSetPagination
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = ""   
        if 'teacher_id' in self.kwargs:
            teacher_id = self.kwargs['teacher_id']
            teacher = models.User.objects.get(pk=teacher_id)
            return models.StudentCourseEnrollment.objects.filter(course__teacher=teacher).distinct()
       

class EnrolledStuentPkList(generics.ListCreateAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = serializers.StudentCourseEnrollSerializer
    pagination_class = StandardResultSetPagination
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = ""
        if 'student_id' in self.kwargs:
            student_id = self.kwargs['student_id']
            student = models.User.objects.get(pk=student_id)
            return models.StudentCourseEnrollment.objects.filter(student=student).distinct()
        
       

class EnrolledStuentCoursesNotaAllPkList(generics.ListCreateAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = serializers.StudentCourseNotAllEnrollSerializer
    pagination_class = StandardResultSetPagination
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = ""
        if 'student_id' in self.kwargs:
            student_id = self.kwargs['student_id']
            student = models.User.objects.get(pk=student_id)
            return models.StudentCourseEnrollment.objects.filter(student=student).distinct()
        


    

class EnrolledRecomemdedStuentList(generics.ListCreateAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = serializers.StudentCourseEnrollSerializer
    pagination_class = StandardResultSetPagination
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = ""

        if 'studentId' in self.kwargs:
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
    # permission_classes = [IsAuthenticated]


class CourseRatingPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CourseRating.objects.all()
    serializer_class = serializers.CourseRatingSerializer
    # permission_classes = [IsAuthenticated]




class CourseRatingListAPI(generics.ListCreateAPIView):
    queryset = models.CourseRating.objects.all()
    serializer_class = serializers.CourseRatingSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

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

# class FetchRatingStatusView(generics.RetrieveAPIView):
class FetchRatingStatusView(APIView):
    # pagination_class = StandardResultSetPagination

    def get(self, request, student_id, course_id):
        student = models.User.objects.filter(id=student_id).first()
        course = models.Course.objects.filter(id=course_id).first()
        rating_status = models.CourseRating.objects.filter(course=course, student=student).exists()
        return Response({'bool': rating_status})





# ******************************************************************************
# ==============================================================================
# *** Student Favorite Course ***
class StudentFavoriteCourseList(generics.ListCreateAPIView):
    queryset = models.StudentFavoriteCourse.objects.all()
    serializer_class = serializers.StudentFavoriteCourseSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]


class StudentFavoriteCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.StudentFavoriteCourse.objects.all()
    serializer_class = serializers.StudentFavoriteCourseSerializer
    # permission_classes = [IsAuthenticated]



class StudentFavoriteCourseListAPI(generics.ListCreateAPIView):
    queryset = models.StudentFavoriteCourse.objects.all()
    serializer_class = serializers.StudentFavoriteCourseSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]
    
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


class RemoveFavoriteCourseView(generics.DestroyAPIView):    
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]
    
    def delete(self, request, course_id, student_id):
        student = models.User.objects.filter(id=student_id).first()
        course = models.Course.objects.filter(id=course_id).first()
        favorite_status = models.StudentFavoriteCourse.objects.filter(course=course, student=student).delete()
        return Response({'bool': favorite_status[0] > 0})






# ******************************************************************************
# ==============================================================================
# *** Teacher Student Chat ***
class TeacherStudentChatList(generics.ListCreateAPIView):
    queryset = models.TeacherStudentChat.objects.all()
    serializer_class = serializers.TeacherStudentChatSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]


class TeacherStudentChatPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.TeacherStudentChat.objects.all()
    serializer_class = serializers.TeacherStudentChatSerializer
    # permission_classes = [IsAuthenticated]



# @csrf_exempt
# def TeacherStudentChatBot(request,teacher_id,student_id):
#     teacher = models.User.objects.get(id=teacher_id)
#     student = models.User.objects.get(id=student_id)
#     msg_to = request.POST.get('msg_to')
#     msg_from = request.POST.get('msg_from')
#     print("\n\n\n\n\n")
#     print("teacher", teacher)
#     print("student", student)
#     print("request", request)
#     print("msg_to", request.POST.get('msg_to'))
#     print("msg_from", request.POST.get('msg_from'))
#     print("\n\n\n\n\n")
#     msg_res = models.TeacherStudentChat.objects.create(
#         teacher=teacher,
#         student=student,
#         msg_to=msg_to,
#         msg_from=msg_from
#     )

#     if msg_res:
#         return JsonResponse({'bool':True,'msg':'Message sended'})
#     else:
#         return JsonResponse({'bool':False,'msg':'Message failed'})




# class TeacherStudentChatBot(generics.CreateAPIView):
#     serializer_class = serializers.TeacherStudentChatSerializer

#     def post(self, request, teacher_id, student_id):
#         teacher = models.User.objects.get(id=teacher_id)
#         student = models.User.objects.get(id=student_id)
        
#         print("\n\n\n\n\n")
#         print("teacher", teacher)
#         print("student", student)
#         print("request", request.data)
#         # print("msg_from", msg_from)
#         print("\n\n\n\n\n")
#         print("\n\n\n\n\n")

#         serializer = self.get_serializer(data=request.data)
#         print("serializer", serializer)
#         print("\n\n\n\n\n")
#         serializer.is_valid(raise_exception=True)
#         serializer.save(teacher=teacher, student=student)

#         return Response({'bool': True, 'msg': 'Message sent'}, status=status.HTTP_201_CREATED)




# class TeacherStudentChatBot(generics.CreateAPIView):
#     serializer_class = serializers.TeacherStudentChatSerializer

#     def post(self, request, teacher_id, student_id):
#         teacher = get_object_or_404(models.User, id=teacher_id)
#         student = get_object_or_404(models.User, id=student_id)

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(teacher=teacher, student=student)

#         return Response({'bool': True, 'msg': 'Message sent'}, status=status.HTTP_201_CREATED)




class TeacherStudentChatBot(generics.CreateAPIView):
    serializer_class = serializers.TeacherStudentChatSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, teacher_id, student_id):
        try:
            # Validate participants
            # teacher = get_object_or_404(models.User, id=teacher_id, user_type='teacher')
            # student = get_object_or_404(models.User, id=student_id, user_type='student')
            
            # # Check if the authenticated user is either the teacher or student
            # if request.user not in [teacher, student]:
            #     return Response(
            #         {"error": "You are not authorized to send messages in this chat"},
            #         status=status.HTTP_403_FORBIDDEN
            #     )

            # Prepare chat data
            chat_data = {
                'teacher': teacher_id,
                'student': student_id,
                'msg_to': request.data.get('msg_to'),
                'msg_from': request.data.get('msg_from'),
            }

            serializer = self.get_serializer(data=chat_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            headers = self.get_success_headers(serializer.data)
            return Response({
                "bool": True,
                "msg": "Message sent successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            return Response({
                "bool": False,
                "msg": str(e),
                "error": "Failed to send message"
            }, status=status.HTTP_400_BAD_REQUEST)
    


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








class TeacherAllChatListAPI(generics.ListAPIView):
    queryset = models.TeacherStudentChat.objects.all()
    serializer_class = serializers.TeacherStudentChatSerializer

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id'] 
        teacher = models.User.objects.get(pk=teacher_id) 
        return models.TeacherStudentChat.objects.filter(teacher=teacher)



class TeacherStudentChatListView(APIView):
    """
    View لعرض قائمة فريدة بكل معلم والطلاب الذين تحدث معهم.
    """
    def get(self, request, *args, **kwargs):
        # 1. إنشاء قاموس لتخزين الطلاب لكل معلم
        #    استخدام set يضمن عدم وجود تكرار للطلاب
        teacher_students_map = {}

        # 2. جلب جميع محادثات الشات
        #    select_related يقوم بتحسين الأداء عن طريق جلب بيانات المعلم والطالب في استعلام واحد
        chats = models.TeacherStudentChat.objects.select_related('teacher', 'student').all()

        # 3. المرور على جميع المحادثات وتجميع البيانات
        for chat in chats:
            teacher_id = chat.teacher.id
            student = chat.student

            if teacher_id not in teacher_students_map:
                # إذا كان هذا أول ظهور للمعلم، قم بإنشاء إدخال جديد له
                teacher_students_map[teacher_id] = {
                    'teacher': chat.teacher,
                    'students': set() # استخدم set لتجنب تكرار الطلاب
                }
            
            # أضف الطالب إلى مجموعة الطلاب الخاصة بالمعلم
            teacher_students_map[teacher_id]['students'].add(student)

        # 4. تحويل البيانات المجمعة إلى قائمة من القواميس
        #    وتحويل مجموعة الطلاب (set) إلى قائمة (list)
        results = [
            {
                'teacher': data['teacher'],
                'students': list(data['students'])
            }
            for data in teacher_students_map.values()
        ]

        # 5. استخدام الـ Serializer لتحويل البيانات إلى JSON
        serializer = serializers.TeacherWithStudentsSerializer(results, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)



class TeacherSpecificStudentsListView(APIView):
    """
    View لعرض قائمة فريدة بالطلاب الذين تواصل معهم معلم معين.
    """
    def get(self, request, teacher_id, *args, **kwargs):
        # 1. التحقق من وجود المعلم، وإرجاع خطأ 404 إذا لم يكن موجودًا
        teacher = get_object_or_404(models.User, id=teacher_id)

        # 2. جلب جميع الطلاب الفريدين الذين لديهم محادثات مع هذا المعلم
        #    - نقوم بتصفية المحادثات حسب `teacher_id`.
        #    - `values_list('student_id', flat=True)`: نختار فقط IDs الطلاب.
        #    - `.distinct()`: هذا هو الجزء الأهم، يضمن عدم تكرار IDs الطلاب.
        student_ids = models.TeacherStudentChat.objects.filter(
            teacher=teacher
        ).values_list('student_id', flat=True).distinct()

        # 3. الآن، جلب كائنات المستخدمين (الطلاب) بناءً على الـ IDs التي حصلنا عليها
        students = models.User.objects.filter(id__in=student_ids)

        # 4. استخدام الـ Serializer لتحويل بيانات الطلاب إلى JSON
        #    `many=True` لأننا نعرض قائمة من الطلاب
        serializer = UserSerializer(students, many=True)
        
        # 5. إرجاع البيانات كاستجابة
        return Response(serializer.data, status=status.HTTP_200_OK)






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
    # p.drawCentredString(width/2, height-150, "شهادة إنجاز")
    p.drawCentredString(width/2, height-150, "Certificate of Achievement")
    
    p.setFont("Helvetica", 18)
    # p.drawCentredString(width/2, height-200, "تعلن منصة الريادة بأن")
    p.drawCentredString(width/2, height-200, "The Entrepreneurship Platform announces that")
    
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width/2, height-250, f"{enrollment.student.get_full_name()}")
    
    p.setFont("Helvetica", 16)
    # p.drawCentredString(width/2, height-300, "قد أكمل بنجاح دورة")
    p.drawCentredString(width/2, height-300, "I have successfully completed the course")
    
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width/2, height-350, f"{enrollment.course.title}")
    
    p.setFont("Helvetica", 14)
    # p.drawCentredString(width/2, height-400, f"بتاريخ: {enrollment.completion_date.strftime('%Y-%m-%d')}")
    p.drawCentredString(width/2, height-400, f"On The Date: {enrollment.completion_date.strftime('%Y-%m-%d')}")
    
    p.setFont("Helvetica", 12)
    p.drawCentredString(width/2, 100, f"Certificate Number: {enrollment.certificate_id}")
    
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
    # permission_classes = [IsAuthenticated]
    
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
# # *** Question Bank ***
# # https://chat.deepseek.com/a/chat/s/213f735f-4a29-4eff-b6e7-72262c349c91
# class QuestionBankList(generics.ListCreateAPIView):
#     queryset = models.QuestionBank.objects.all()
#     serializer_class = serializers.QuestionBankSerializer
#     pagination_class = StandardResultSetPagination
#     permission_classes = [AllowAny]
#     # permission_classes = [IsAuthenticated]

#     # def get_queryset(self):
#     #     if self.request.user.is_student:
#     #         return models.QuestionBank.objects.filter(user=self.request.user)
#     #     return models.QuestionBank.objects.all()

#     # def get_queryset(self):
#     #     user = self.request.user
#     #     if user.is_student:
#     #         return models.QuestionBank.objects.filter(user=user)
#     #     return models.QuestionBank.objects.all()


# class QuestionBankPK(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.QuestionBank.objects.all()
#     serializer_class = serializers.QuestionBankSerializer
#     # permission_classes = [IsAuthenticated]

#     # def get_queryset(self):
#     #     # هذه السطر يحل مشكلة إنشاء schema
#     #     if getattr(self, 'swagger_fake_view', False):
#     #         return models.QuestionBank.objects.none()
        
#     #     user = self.request.user
#     #     if user.is_superuser:
#     #         return models.QuestionBank.objects.all()
#     #     else:
#     #         return models.QuestionBank.objects.filter(user=user)



# class QuestionBankViewSet(viewsets.ModelViewSet):
#     queryset = models.QuestionBank.objects.all()
    
#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return serializers.QuestionBankDetailSerializer
#         return serializers.QuestionBankSerializer
    
#     @action(detail=True, methods=['get'])
#     def questions(self, request, pk=None):
#         """Get all questions for a question bank"""
#         question_bank = self.get_object()
#         questions = question_bank.questions.all()
#         serializer = serializers.QuestionBankSerializer(questions, many=True)
#         return Response(serializer.data)
    
#     @action(detail=True, methods=['get'])
#     def quiz(self, request, pk=None):
#         """Get randomized questions for quiz taking"""
#         question_bank = self.get_object()
#         questions = list(question_bank.questions.all())
        
#         # Randomize questions
#         random.shuffle(questions)
        
#         # Serialize questions but exclude is_correct from choices
#         serialized_questions = []
#         for question in questions:
#             question_data = serializers.QuestionBankSerializer(question).data
            
#             # Remove is_correct field from choices
#             for choice in question_data['choices']:
#                 if 'is_correct' in choice:
#                     del choice['is_correct']
            
#             serialized_questions.append(question_data)
        
#         return Response(serialized_questions)


# class QuestionInBankViewSet(viewsets.ModelViewSet):
#     queryset = models.QuestionInBank.objects.all()
    
#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return serializers.QuestionInBankDetailSerializer
#         return serializers.QuestionInBankSerializer
    
#     def get_queryset(self):
#         queryset = models.QuestionInBank.objects.all()
#         question_bank_id = self.request.query_params.get('question_bank')
        
#         if question_bank_id:
#             queryset = queryset.filter(question_bank_id=question_bank_id)
        
#         return queryset







# ******************************************************************************
# ==============================================================================
# ***   Subscribe Course   ***
class SubscribeCourseList(generics.ListCreateAPIView):
    queryset = models.SubscribeCourse.objects.all()
    serializer_class = serializers.SubscribeCourseSerializer
    pagination_class = StandardResultSetPagination
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_student:
            return models.SubscribeCourse.objects.filter(user=self.request.user)
        return models.SubscribeCourse.objects.all()
    

class SubscribeCourseListApp(generics.ListAPIView):
    queryset = models.SubscribeCourse.objects.all()
    serializer_class = serializers.SubscribeCourseSerializer 
    permission_classes = [AllowAny]


class SubscribeCourseListAdmin(generics.ListCreateAPIView):
    queryset = models.SubscribeCourse.objects.all()
    serializer_class = serializers.SubscribeCourseSerializer 
    pagination_class = StandardResultSetPagination
    permission_classes = [IsAuthenticated]


class SubscribeCourseResultList(generics.ListCreateAPIView):
    queryset = models.SubscribeCourse.objects.all()
    serializer_class = serializers.SubscribeCourseSerializer  

    def get_queryset(self):
        qs = super().get_queryset()
        if 'result' in self.request.GET:
            try:
                limit = int(self.request.GET['result'])
                qs = qs.order_by('-id').filter(is_visible=True)[:limit]
            except ValueError:
                # Handle the case where 'result' is not an integer
                pass
        return qs


class SubscribeCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SubscribeCourse.objects.all()
    serializer_class = serializers.SubscribeCourseSerializer
    permission_classes = [AllowAny]
 
    
  
  

class SubscribeCoursesSearchList(generics.ListCreateAPIView):
    queryset = models.SubscribeCourse.objects.all()
    serializer_class = serializers.SubscribeCourseSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring'] 
            qs = qs.filter(
                Q(status__icontains=search)
                |Q(full_name__icontains=search) 
                |Q(email__icontains=search)  
                )
        return qs

  



# ******************************************************************************
# ==============================================================================
# ***  Documents  *** #
class DocumentList(generics.ListCreateAPIView):
    queryset = models.Document.objects.all()
    serializer_class = serializers.DocumentSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return models.Document.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return models.Document.objects.all()
        else:
            return models.Document.objects.filter(user=user)
     


class DocumentListAdmin(generics.ListCreateAPIView):
    queryset = models.Document.objects.all()
    serializer_class = serializers.DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return models.Document.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return models.Document.objects.all()
        else:
            return models.Document.objects.filter(user=user)


class DocumentListApp(generics.ListAPIView):
    queryset = models.Document.objects.filter(is_visible=True)
    serializer_class = serializers.DocumentSerializer
    permission_classes = [AllowAny]



class DocumentResultList(generics.ListCreateAPIView):
    queryset = models.Document.objects.all()
    serializer_class = serializers.DocumentSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if 'result' in self.request.GET:
            try:
                limit = int(self.request.GET['result'])
                qs = qs.order_by('-id').filter(is_visible=True)[:limit]
            except ValueError:
                # Handle the case where 'result' is not an integer
                pass
        return qs
    


class DocumentPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Document.objects.all()
    serializer_class = serializers.DocumentSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]


class DocumentSearchList(generics.ListCreateAPIView):
    queryset = models.Document.objects.all()
    serializer_class = serializers.DocumentSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring'] 
            qs = qs.filter(
                Q(title__icontains=search)
                |Q(description__icontains=search)
                )
        return qs



class DocumentSectionList(generics.ListCreateAPIView):
    queryset = models.SectionCourse.objects.all()
    serializer_class = serializers.DocumentSerializer
    # pagination_class = StandardResultSetPagination
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        section_id = self.kwargs["pk"]
        section = models.SectionCourse.objects.get(id=section_id)
        return models.Document.objects.filter(section=section)










class DocumentFileList(generics.ListCreateAPIView):
    serializer_class = serializers.DocumentFileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        document_id = self.kwargs.get('document_id')
        return models.DocumentFile.objects.filter(document_id=document_id)
    
    def perform_create(self, serializer):
        document_id = self.kwargs.get('document_id')
        document = models.Document.objects.get(id=document_id)
        
        # التحقق من أن المستخدم يملك المستند
        if not self.request.user.is_superuser and document.user != self.request.user:
            raise PermissionDenied("You don't have permission to add files to this document")
        
        file = self.request.FILES.get('file')
        serializer.save(
            document=document,
            file_name=file.name,
            file_size=file.size,
            file_type=file.content_type
        )


class DocumentFileDetail(generics.RetrieveDestroyAPIView):
    serializer_class = serializers.DocumentFileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return models.DocumentFile.objects.all()
        else:
            return models.DocumentFile.objects.filter(document__user=user)









# ******************************************************************************
# ==============================================================================
# ***    *** #
# Question Bank Views
class QuestionBankList(generics.ListCreateAPIView):
    queryset = models.QuestionBank.objects.all()
    serializer_class = serializers.QuestionBankSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]

    # def get_serializer_class(self):
    #     return serializers.QuestionBankSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    # def get_queryset(self):
    #     if self.request.user.is_staff:
    #         return self.queryset
    #     return self.queryset.filter(user=self.request.user)


    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return models.QuestionBank.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return models.QuestionBank.objects.all()
        else:
            return models.QuestionBank.objects.filter(user=user)
        


class QuestionBankListAdmin(generics.ListCreateAPIView):
    queryset = models.QuestionBank.objects.all()
    serializer_class = serializers.QuestionBankSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return models.QuestionBank.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return models.QuestionBank.objects.all()
        else:
            return models.QuestionBank.objects.filter(user=user)


class QuestionBankListApp(generics.ListCreateAPIView):
    queryset = models.QuestionBank.objects.filter(is_visible=True)
    serializer_class = serializers.QuestionBankSerializer
    permission_classes = [AllowAny]



class QuestionBankResultList(generics.ListCreateAPIView):
    queryset = models.QuestionBank.objects.all()
    serializer_class = serializers.QuestionBankSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if 'result' in self.request.GET:
            try:
                limit = int(self.request.GET['result'])
                qs = qs.order_by('-id').filter(is_visible=True)[:limit]
            except ValueError:
                # Handle the case where 'result' is not an integer
                pass
        return qs
    


class QuestionBankRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.QuestionBank.objects.all()
    serializer_class = serializers.QuestionBankSerializer
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     # هذه السطر يحل مشكلة إنشاء schema
    #     if getattr(self, 'swagger_fake_view', False):
    #         return models.QuestionBank.objects.none()
        
    #     user = self.request.user
    #     if user.is_superuser:
    #         return models.QuestionBank.objects.all()
    #     else:
    #         return models.QuestionBank.objects.filter(user=user)

    # permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return serializers.QuestionBankDetailSerializer
    #     return serializers.QuestionBankSerializer



# Custom Views for Relationships
class BankQuestionsListView(generics.ListAPIView):
    serializer_class = serializers.QuestionInBankSerializer
    # pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        bank_id = self.kwargs['bank_id']
        return models.QuestionInBank.objects.filter(question_bank=bank_id)











# Question Views
class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = models.QuestionInBank.objects.all()
    serializer_class = serializers.QuestionInBankDetailSerializer
    # pagination_class = StandardResultSetPagination
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.QuestionInBankDetailSerializer
        return serializers.QuestionInBankSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        # if not self.request.user.is_staff:
        #     queryset = queryset.filter(user=self.request.user)
        
        bank_id = self.request.query_params.get('bank')
        if bank_id:
            queryset = queryset.filter(bank_id=bank_id)
        
        return queryset




# Question Views
class QuestionListCreate(generics.ListCreateAPIView):
    queryset = models.QuestionInBank.objects.all()
    serializer_class = serializers.QuestionInBankSerializer
    # pagination_class = StandardResultSetPagination
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]



class QuestionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.QuestionInBank.objects.all()
    serializer_class = serializers.QuestionInBankSerializer    
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    # def get_serializer_class(self):
    #     if self.request.method in ['PUT', 'PATCH']:
    #         return serializers.QuestionInBankDetailSerializer
    #     return serializers.QuestionInBankSerializer




class QuestionChoicesListView(generics.ListAPIView):
    serializer_class = serializers.ChoiceQuestionInBankSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        question_id = self.kwargs['question_id']
        return models.ChoiceQuestionInBank.objects.filter(question=question_id)


class QuestionInBankSearchList(generics.ListCreateAPIView):
    queryset = models.QuestionInBank.objects.all()
    serializer_class = serializers.QuestionInBankSerializer
    # pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring'] 
            qs = qs.filter(
                Q(text__icontains=search)
                # |Q(description__icontains=search)
                )
        return qs
    



class BanksQuestionInBankSearchList(generics.ListAPIView):
    queryset = models.QuestionInBank.objects.all()
    serializer_class = serializers.QuestionInBankSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        bank_id = self.kwargs['bank_id']
        search = self.kwargs['searchstring']
        qs = qs.filter(question_bank_id=bank_id).filter(
            Q(text__icontains=search)
        )
        return qs



# Choice Views
class ChoiceListCreateView(generics.ListCreateAPIView):
    queryset = models.ChoiceQuestionInBank.objects.all()
    serializer_class = serializers.ChoiceQuestionInBankSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        # if not self.request.user.is_staff:
        #     queryset = queryset.filter(user=self.request.user)
        
        question_id = self.request.query_params.get('question')
        if question_id:
            queryset = queryset.filter(question_id=question_id)
        
        return queryset



class ChoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ChoiceQuestionInBank.objects.all()
    serializer_class = serializers.ChoiceQuestionInBankSerializer
    # permission_classes = [IsAuthenticated, IsOwnerOrAdmin]










# ******************************************************************************
# ==============================================================================
# ***   *** #
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








# ******************************************************************************
# ==============================================================================
# ***   *** #

# class QuestionBankResultView(APIView):
#     def post(self, request, question_bank_id):
#         """Calculate quiz results"""
#         # Get the question bank
#         question_bank = get_object_or_404(models.QuestionBank, pk=question_bank_id)
        
#         # Get all questions for this bank
#         all_questions = models.QuestionInBank.objects.filter(question_bank=question_bank_id)
        
#         # Validate the request data
#         serializer = serializers.QuestionBankResultSerializer(data=request.data, many=True)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         # Process the results
#         submitted_answers = {answer['question_id']: answer['selected_choice_id'] for answer in serializer.validated_data}
#         total_questions = all_questions.count()
#         correct_answers = 0
#         results = []
        
#         for question in all_questions:
#             question_id = question.id
#             selected_choice_id = submitted_answers.get(question_id)
            
#             # Get the correct choice
#             correct_choice = question.choices.filter(is_correct=True).first()
            
#             # Check if the answer is correct (only if answered)
#             is_answered = question_id in submitted_answers
#             is_correct = False
            
#             if is_answered and correct_choice:
#                 is_correct = correct_choice.id == selected_choice_id
#                 if is_correct:
#                     correct_answers += 1
            
#             # Add to results
#             results.append({
#                 'question_id': question_id,
#                 'question_text': question.text,
#                 'is_answered': is_answered,
#                 'selected_choice_id': selected_choice_id,
#                 'correct_choice_id': correct_choice.id if correct_choice else None,
#                 'is_correct': is_correct,
#                 'choices': [
#                     {
#                         'id': choice.id,
#                         'text': choice.text,
#                         'is_correct': choice.is_correct
#                     }
#                     for choice in question.choices.all()
#                 ]
#             })
        
#         # Calculate percentage
#         percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
#         return Response({
#             'total_questions': total_questions,
#             'answered_questions': len(submitted_answers),
#             'correct_answers': correct_answers,
#             'percentage': round(percentage, 2),
#             'results': results
#         })


# # 
# class StudentQuestionBankResultSaveView(APIView):
#     # permission_classes = [IsAuthenticated]

#     def post(self, request, question_bank_id):
#         question_bank = get_object_or_404(models.QuestionBank, pk=question_bank_id)
        
#         result_data = {
#             'user': request.user.id,
#             'question_bank': question_bank.id,
#             'answered_questions': request.data.get('answered_questions'),
#             'correct_answers': request.data.get('correct_answers'),
#             'percentage': request.data.get('percentage'),
#             'total_questions': request.data.get('total_questions'),
#         }
        
#         result_serializer = serializers.StudentQuestionBankResultSerializer(data=result_data)
#         if not result_serializer.is_valid():
#             return Response(result_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         quiz_result = result_serializer.save()
        
#         answers_data = request.data.get('results', [])
#         for answer_data in answers_data:
#             selected_choice = next(
#                 (c for c in answer_data.get('choices', []) if c['id'] == answer_data.get('selected_choice_id')),
#                 None
#             )
#             correct_choice = next(
#                 (c for c in answer_data.get('choices', []) if c.get('is_correct', False)),
#                 None
#             )
            
#             answer_data['quiz_result'] = quiz_result.id
#             answer_data['selected_choice_text'] = selected_choice['text'] if selected_choice else None
#             answer_data['correct_choice_text'] = correct_choice['text'] if correct_choice else None
#             answer_data['all_choices'] = answer_data.get('choices', [])
            
#             answer_serializer = serializers.StudentQuestionBankAnswerSerializer(data=answer_data)
#             if answer_serializer.is_valid():
#                 answer_serializer.save()
        
#         return Response({
#             'status': 'success',
#             'result_id': quiz_result.id
#         }, status=status.HTTP_201_CREATED)
    






# ******************************************************************************
# ==============================================================================
# ***   *** #

# class QuestionBankResultView(APIView):
#     def post(self, request, question_bank_id):
#         question_bank = get_object_or_404(models.QuestionBank, pk=question_bank_id)
#         questions = models.QuestionInBank.objects.filter(question_bank=question_bank)
        
#         serializer = serializers.QuestionBankResultSerializer(data=request.data, many=True)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         submitted_answers = {answer['question_id']: answer['selected_choice_id'] for answer in serializer.validated_data}
#         total_questions = questions.count()
#         correct_answers = 0
#         results = []
        
#         for question in questions:
#             question_id = question.id
#             selected_choice_id = submitted_answers.get(question_id)
#             is_answered = selected_choice_id is not None
#             is_correct = False
            
#             if is_answered:
#                 # تحقق مما إذا كان الخيار المحدد هو الصحيح
#                 correct_index = question.correct_answer
#                 if correct_index < len(question.choices):
#                     is_correct = selected_choice_id == correct_index
#                     if is_correct:
#                         correct_answers += 1
            
#             # إعداد بيانات النتيجة
#             result_data = {
#                 'question_id': question_id,
#                 'question_text': question.text,
#                 'is_answered': is_answered,
#                 'selected_choice_id': selected_choice_id,
#                 'correct_choice_id': question.correct_answer,
#                 'is_correct': is_correct,
#                 'all_choices': question.choices,
#             }
#             results.append(result_data)
        
#         # حساب النسبة المئوية
#         percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
#         return Response({
#             'total_questions': total_questions,
#             'answered_questions': len(submitted_answers),
#             'correct_answers': correct_answers,
#             'percentage': round(percentage, 2),
#             'results': results
#         })
    

# class StudentQuestionBankResultSaveView(APIView):
#     def post(self, request, question_bank_id):
#         question_bank = get_object_or_404(models.QuestionBank, pk=question_bank_id)
#         user = request.user
        
#         # حفظ النتيجة الرئيسية
#         result_data = {
#             'user': user.id,
#             'question_bank': question_bank.id,
#             'answered_questions': request.data.get('answered_questions'),
#             'correct_answers': request.data.get('correct_answers'),
#             'percentage': request.data.get('percentage'),
#             'total_questions': request.data.get('total_questions'),
#         }
        
#         result_serializer = serializers.StudentQuestionBankResultSerializer(data=result_data)
#         if not result_serializer.is_valid():
#             return Response(result_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         quiz_result = result_serializer.save()
        
#         # حفظ الإجابات التفصيلية
#         answers_data = request.data.get('results', [])
#         for answer_data in answers_data:
#             answer_data['question_bank_result'] = quiz_result.id
            
#             # الحصول على نص الخيار المحدد والصحيح
#             selected_choice_text = None
#             correct_choice_text = None
            
#             if answer_data.get('selected_choice_id') is not None:
#                 selected_choice = answer_data['all_choices'][answer_data['selected_choice_id']]
#                 selected_choice_text = selected_choice.get('text')
            
#             if answer_data.get('correct_choice_id') is not None:
#                 correct_choice = answer_data['all_choices'][answer_data['correct_choice_id']]
#                 correct_choice_text = correct_choice.get('text')
            
#             answer_data.update({
#                 'selected_choice_text': selected_choice_text,
#                 'correct_choice_text': correct_choice_text,
#             })
            
#             answer_serializer = serializers.StudentQuestionBankAnswerSerializer(data=answer_data)
#             if answer_serializer.is_valid():
#                 answer_serializer.save()
        
#         return Response({
#             'status': 'success',
#             'result_id': quiz_result.id
#         }, status=status.HTTP_201_CREATED)


# ******************************************************************************
# ==============================================================================
# 

# class QuestionBankResultView(APIView):
#     def post(self, request, question_bank_id):
#         question_bank = get_object_or_404(models.QuestionBank, pk=question_bank_id)
#         questions = models.QuestionInBank.objects.filter(question_bank=question_bank)
        
#         serializer = serializers.QuestionBankResultSerializer(data=request.data, many=True)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         submitted_answers = {answer['question_id']: answer['selected_choice_id'] for answer in serializer.validated_data}
#         total_questions = questions.count()
#         correct_answers = 0
#         results = []
        
#         for question in questions:
#             question_id = question.id
#             selected_choice_id = submitted_answers.get(question_id)
#             is_answered = selected_choice_id is not None
#             is_correct = False
            
#             if is_answered:
#                 # تحقق مما إذا كان الخيار المحدد هو الصحيح
#                 correct_index = question.correct_answer
#                 if correct_index < len(question.choices):
#                     is_correct = selected_choice_id == correct_index
#                     if is_correct:
#                         correct_answers += 1
            
#             # إعداد بيانات النتيجة
#             result_data = {
#                 'question_id': question_id,
#                 'question_text': question.text,
#                 'is_answered': is_answered,
#                 'selected_choice_id': selected_choice_id,
#                 'correct_choice_id': question.correct_answer,
#                 'is_correct': is_correct,
#                 'all_choices': question.choices,
#             }
#             results.append(result_data)
        
#         # حساب النسبة المئوية
#         percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
#         return Response({
#             'total_questions': total_questions,
#             'answered_questions': len(submitted_answers),
#             'correct_answers': correct_answers,
#             'percentage': round(percentage, 2),
#             'results': results
#         })

# class StudentQuestionBankResultSaveView(APIView):
#     def post(self, request, question_bank_id):
#         question_bank = get_object_or_404(models.QuestionBank, pk=question_bank_id)
#         user = request.user
        
#         # حفظ النتيجة الرئيسية
#         result_data = {
#             'user': user.id,
#             'question_bank': question_bank.id,
#             'answered_questions': request.data.get('answered_questions'),
#             'correct_answers': request.data.get('correct_answers'),
#             'percentage': request.data.get('percentage'),
#             'total_questions': request.data.get('total_questions'),
#         }
        
#         result_serializer = serializers.StudentQuestionBankResultSerializer(data=result_data)
#         if not result_serializer.is_valid():
#             return Response(result_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         quiz_result = result_serializer.save()
        
#         # حفظ الإجابات التفصيلية
#         answers_data = request.data.get('results', [])
#         for answer_data in answers_data:
#             answer_data['question_bank_result'] = quiz_result.id
            
#             # الحصول على نص الخيار المحدد والصحيح
#             selected_choice_text = None
#             correct_choice_text = None
            
#             if answer_data.get('selected_choice_id') is not None:
#                 selected_choice = answer_data['all_choices'][answer_data['selected_choice_id']]
#                 selected_choice_text = selected_choice.get('text')
            
#             if answer_data.get('correct_choice_id') is not None:
#                 correct_choice = answer_data['all_choices'][answer_data['correct_choice_id']]
#                 correct_choice_text = correct_choice.get('text')
            
#             answer_data.update({
#                 'selected_choice_text': selected_choice_text,
#                 'correct_choice_text': correct_choice_text,
#             })
            
#             answer_serializer = serializers.StudentQuestionBankAnswerSerializer(data=answer_data)
#             if answer_serializer.is_valid():
#                 answer_serializer.save()
        
#         return Response({
#             'status': 'success',
#             'result_id': quiz_result.id
#         }, status=status.HTTP_201_CREATED)








# ******************************************************************************
# ==============================================================================
# 


class StudentQuestionBankResultListApp(generics.ListCreateAPIView):
    queryset = models.StudentQuestionBankResult.objects.all()
    serializer_class = serializers.StudentQuestionBankResultSerializer
    permission_classes = [AllowAny]
    # pagination_class = StandardResultSetPagination


class StudentQuestionBankResultPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.StudentQuestionBankResult.objects.all()
    serializer_class = serializers.StudentQuestionBankResultSerializer
    permission_classes = [AllowAny]


class StudentQuestionBankResultBankList(generics.ListAPIView):
    serializer_class = serializers.StudentQuestionBankResultSerializer
    # pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        bank_id = self.kwargs['bank_id']
        return models.StudentQuestionBankResult.objects.filter(question_bank=bank_id)


class StudentQuestionBankResultUserList(generics.ListAPIView):
    serializer_class = serializers.StudentQuestionBankResultSerializer
    # pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return models.StudentQuestionBankResult.objects.filter(user=user_id)







# ******************************************************************************
# ==============================================================================
# ***   *** #
# 
class QuestionBankSearchList(generics.ListCreateAPIView):
    queryset = models.QuestionBank.objects.all()
    serializer_class = serializers.QuestionBankSerializer
    # pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring'] 
            qs = qs.filter(
                Q(title__icontains=search)
                |Q(description__icontains=search)
                )
        return qs
    






# ******************************************************************************
# ==============================================================================
# ***  ***
class QuestionBankSectionList(generics.ListCreateAPIView):
    queryset = models.SectionCourse.objects.all()
    serializer_class = serializers.QuestionBankSerializer
    # pagination_class = StandardResultSetPagination
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        section_id = self.kwargs["pk"]
        section = models.SectionCourse.objects.get(id=section_id)
        return models.QuestionBank.objects.filter(section=section)






# ******************************************************************************
# ==============================================================================
# ***  ***















# ******************************************************************************
# ==============================================================================
# *** ContactUs ***
# (List of contact us -> [GET, POST])
class ContactUsListAPIView(generics.ListCreateAPIView):
    queryset = models.ContactUsUser.objects.all()
    serializer_class = serializers.ContactUsUserSerializer
    pagination_class = StandardResultSetPagination
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_student:
            return models.ContactUsUser.objects.filter(user=self.request.user)
        return models.ContactUsUser.objects.all()

    # def get_queryset(self):
    #     if self.request.user:
    #         user = self.request.user
    #         if user.is_student:
    #             return models.ContactUsUser.objects.filter(user=user)
    #         else:
    #             return models.ContactUsUser.objects.all()
    
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_authenticated:
    #         if user.is_student:
    #             return models.ContactUsUser.objects.filter(user=user)
    #         else:
    #             return models.ContactUsUser.objects.all()
    #     else:
    #         return models.ContactUsUser.objects.none


# (List of contact us -> [GET, POST, PUT, DELETE])
class ContactUsPKAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ContactUsUser.objects.all()
    serializer_class = serializers.ContactUsUserSerializer
    permission_classes = [IsAuthenticated]

    
    def get_queryset(self):
        #     # هذه السطر يمنع المشكلة أثناء إنشاء schema لوثائق API
        if getattr(self, 'swagger_fake_view', False):
            return models.ContactUsUser.objects.none()
        
        if self.request.user.is_student:
            return models.ContactUsUser.objects.filter(user=self.request.user)
        return models.ContactUsUser.objects.all()

    # def get_queryset(self):
    #     # هذه السطر يمنع المشكلة أثناء إنشاء schema لوثائق API
    #     if getattr(self, 'swagger_fake_view', False):
    #         return models.ReviewUser.objects.none()
        
    #     user = self.request.user
    #     if user.is_student:
    #         return models.ContactUsUser.objects.filter(user=user)
    #     else:
    #         return models.ContactUsUser.objects.all()


# 
class ContactusUserSearchList(generics.ListCreateAPIView):
    queryset = models.ContactUsUser.objects.all()
    serializer_class = serializers.ContactUsUserSerializer
    pagination_class = StandardResultSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_student:
            qs = models.ContactUsUser.objects.filter(user=self.request.user)
        else:
            qs = models.ContactUsUser.objects.all()

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring'] 
            qs = qs.filter(
                Q(full_name__icontains=search)
                |Q(email__icontains=search)
                |Q(titleofmessage__icontains=search)
                |Q(message__icontains=search)
                )
        return qs



# class ContactusUserSearchList(generics.ListCreateAPIView):
#     queryset = models.ContactUsUser.objects.all()
#     serializer_class = serializers.ContactUsUserSerializer
#     pagination_class = StandardResultSetPagination
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         if self.request.user.is_student:
#             qs = models.ContactUsUser.objects.filter(user=self.request.user)
#         else:
#             qs = models.ContactUsUser.objects.all()

#         search = self.request.GET.get('searchstring')
#         if search:
#             qs = qs.filter(
#                 Q(full_name__icontains=search) |
#                 Q(email__icontains=search) |
#                 Q(titleofmessage__icontains=search) |
#                 Q(message__icontains=search)
#             )
#         return qs


# ******************************************************************************
# ==============================================================================
# *** Review ***
# (List of review -> [GET, POST])
class ReviewUserListAPIView(generics.ListCreateAPIView):
    queryset = models.ReviewUser.objects.all()
    serializer_class = serializers.ReviewUserSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_student:
            return models.ReviewUser.objects.filter(user=self.request.user)
        return models.ReviewUser.objects.all()

    # def get_queryset(self):
    #     if self.request.user.is_authenticated:
    #         if self.request.user.is_student:
    #             return models.ReviewUser.objects.filter(user=self.request.user)
    #         else:
    #             return models.ReviewUser.objects.all()
    #     else:
    #         # يمكنك إرجاع queryset فارغ أو رفع استثناء إذا لم يكن المستخدم مصادقًا عليه
    #         return models.ReviewUser.objects.none()


class ReviewUserListApp(generics.ListCreateAPIView):
    queryset = models.ReviewUser.objects.all()
    serializer_class = serializers.ReviewUserSerializer
    permission_classes = [AllowAny]



class ReviewUserResultList(generics.ListCreateAPIView):
    queryset = models.ReviewUser.objects.all()
    serializer_class = serializers.ReviewUserSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if 'result' in self.request.GET:
            try:
                limit = int(self.request.GET['result'])
                qs = qs.order_by('-id').filter(is_visible=True,status="publication")[:limit]
            except ValueError:
                # Handle the case where 'result' is not an integer
                pass
        return qs

# (List of review -> [GET, POST, PUT, DELETE])
class ReviewUserPKAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ReviewUser.objects.all()
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
        

# (List of review -> [GET])
class ReviewUserSearchList(generics.ListCreateAPIView):
    queryset = models.ReviewUser.objects.all()
    serializer_class = serializers.ReviewUserSerializer
    pagination_class = StandardResultSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_student:
            qs = models.ReviewUser.objects.filter(user=self.request.user)
        else:
            qs = models.ReviewUser.objects.all()

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring'] 
            qs = models.ReviewUser.objects.filter(
                Q(status__icontains=search)
                |Q(first_name__icontains=search)
                |Q(message__icontains=search)
                |Q(rating__icontains=search)
                )
        return qs





# ******************************************************************************
# ==============================================================================
# *** Teacher Student Chat ***
class PublicChatList(generics.ListCreateAPIView):
    queryset = models.PublicChat.objects.all()
    serializer_class = serializers.PublicChatSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]


class PublicChatPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.PublicChat.objects.all()
    serializer_class = serializers.PublicChatSerializer
    # permission_classes = [IsAuthenticated]




class PublicChatGetMessageTeacherStudent(generics.ListAPIView):
    queryset = models.PublicChat.objects.all()
    serializer_class = serializers.PublicChatSerializer

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        student_id = self.kwargs['student_id']
        teacher = models.User.objects.get(pk=teacher_id)
        student = models.User.objects.get(pk=student_id)
        return models.PublicChat.objects.filter(teacher=teacher, student=student).exclude(msg_to='')




class PublicChatSendMessageTeacherStudent(generics.CreateAPIView):
    serializer_class = serializers.PublicChatSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, teacher_id, student_id):
        try:
            # Validate participants
            # teacher = get_object_or_404(models.User, id=teacher_id, user_type='teacher')
            # student = get_object_or_404(models.User, id=student_id, user_type='student')
            
            # # Check if the authenticated user is either the teacher or student
            # if request.user not in [teacher, student]:
            #     return Response(
            #         {"error": "You are not authorized to send messages in this chat"},
            #         status=status.HTTP_403_FORBIDDEN
            #     )

            # Prepare chat data
            chat_data = {
                'teacher': teacher_id,
                'student': student_id,
                'msg_to': request.data.get('msg_to'),
                'msg_from': request.data.get('msg_from'),
                'image': request.data.get('image'),
            }

            serializer = self.get_serializer(data=chat_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            
            headers = self.get_success_headers(serializer.data)
            return Response({
                "bool": True,
                "msg": "Message sent successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            return Response({
                "bool": False,
                "msg": str(e),
                "error": "Failed to send message"
            }, status=status.HTTP_400_BAD_REQUEST)
    












class PublicChatTeacherAllChatListAPI(generics.ListAPIView):
    queryset = models.PublicChat.objects.all()
    serializer_class = serializers.PublicChatSerializer

    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id'] 
        teacher = models.User.objects.get(pk=teacher_id) 
        return models.PublicChat.objects.filter(teacher=teacher)



class PublicChatStudentAllChatListAPI(generics.ListAPIView):
    queryset = models.PublicChat.objects.all()
    serializer_class = serializers.PublicChatSerializer

    def get_queryset(self):
        student_id = self.kwargs['student_id'] 
        student = models.User.objects.get(pk=student_id) 
        return models.PublicChat.objects.filter(student=student)








class PublicChatTeacherWithStudentsListView(APIView):
    """
    View لعرض قائمة فريدة بكل معلم والطلاب الذين تحدث معهم.
    """
    def get(self, request, *args, **kwargs):
        # 1. إنشاء قاموس لتخزين الطلاب لكل معلم
        #    استخدام set يضمن عدم وجود تكرار للطلاب
        teacher_students_map = {}

        # 2. جلب جميع محادثات الشات
        #    select_related يقوم بتحسين الأداء عن طريق جلب بيانات المعلم والطالب في استعلام واحد
        chats = models.PublicChat.objects.select_related('teacher', 'student').all()

        # 3. المرور على جميع المحادثات وتجميع البيانات
        for chat in chats:
            teacher_id = chat.teacher.id
            student = chat.student

            if teacher_id not in teacher_students_map:
                # إذا كان هذا أول ظهور للمعلم، قم بإنشاء إدخال جديد له
                teacher_students_map[teacher_id] = {
                    'teacher': chat.teacher,
                    'students': set() # استخدم set لتجنب تكرار الطلاب
                }
            
            # أضف الطالب إلى مجموعة الطلاب الخاصة بالمعلم
            teacher_students_map[teacher_id]['students'].add(student)

        # 4. تحويل البيانات المجمعة إلى قائمة من القواميس
        #    وتحويل مجموعة الطلاب (set) إلى قائمة (list)
        results = [
            {
                'teacher': data['teacher'],
                'students': list(data['students'])
            }
            for data in teacher_students_map.values()
        ]

        # 5. استخدام الـ Serializer لتحويل البيانات إلى JSON
        serializer = serializers.PublicChatTeacherWithStudentsSerializer(results, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)



class PublicChatTeacherSpecificStudentsListView(APIView):
    """
    View لعرض قائمة فريدة بالطلاب الذين تواصل معهم معلم معين.
    """
    def get(self, request, teacher_id, *args, **kwargs):
        # 1. التحقق من وجود المعلم، وإرجاع خطأ 404 إذا لم يكن موجودًا
        teacher = get_object_or_404(models.User, id=teacher_id)

        # 2. جلب جميع الطلاب الفريدين الذين لديهم محادثات مع هذا المعلم
        #    - نقوم بتصفية المحادثات حسب `teacher_id`.
        #    - `values_list('student_id', flat=True)`: نختار فقط IDs الطلاب.
        #    - `.distinct()`: هذا هو الجزء الأهم، يضمن عدم تكرار IDs الطلاب.
        student_ids = models.PublicChat.objects.filter(
            teacher=teacher
        ).values_list('student_id', flat=True).distinct()

        # 3. الآن، جلب كائنات المستخدمين (الطلاب) بناءً على الـ IDs التي حصلنا عليها
        students = models.User.objects.filter(id__in=student_ids)

        # 4. استخدام الـ Serializer لتحويل بيانات الطلاب إلى JSON
        #    `many=True` لأننا نعرض قائمة من الطلاب
        serializer = UserSerializer(students, many=True)
        
        # 5. إرجاع البيانات كاستجابة
        return Response(serializer.data, status=status.HTTP_200_OK)







# ******************************************************************************
# ==============================================================================
# ***  ***






# ******************************************************************************
# ==============================================================================
# *** App Stats ***
class AppStatsView(generics.GenericAPIView):
    def get(self, request):
        users_count = models.User.objects.count()
        admins_count = models.User.objects.filter(is_admin=True).count()
        teachers_count = models.User.objects.filter(is_teacher=True).count()
        staffs_count = models.User.objects.filter(is_superuser=False, is_staff=True).count()
        students_count = models.User.objects.filter(is_student=True).count()

        categories_section_count = models.CategorySection.objects.filter(is_visible=True).count()
        sections_course_count = models.SectionCourse.objects.filter(is_visible=True).count()

        courses_count = models.Course.objects.filter(is_visible=True).count()
        sections_in_course_count = models.SectionInCourse.objects.filter(is_visible=True).count()
        lessons_count = models.LessonInCourse.objects.filter(is_visible=True).count()

        coupons_course_count = models.CouponCourse.objects.filter(is_visible=True).count()
        
        total_enrolled_students = models.StudentCourseEnrollment.objects.count()

        questionbanks_count = models.QuestionBank.objects.filter(is_visible=True).count()


        contacts_count = models.ContactUsUser.objects.count()
        reviews_count = models.ReviewUser.objects.count()

        return Response({
            'users_count': users_count,
            'admins_count': admins_count,
            'teachers_count': teachers_count,
            'staffs_count': staffs_count,
            'students_count': students_count,

            'categories_section_count': categories_section_count,
            'sections_course_count': sections_course_count,

            'courses_count': courses_count,
            'sections_in_course_count': sections_in_course_count,
            'lessons_count': lessons_count,
            
            'coupons_course_count': coupons_course_count,

            'total_enrolled_students': total_enrolled_students,

            'questionbanks_count': questionbanks_count,

            'contacts_count': contacts_count,
            'reviews_count': reviews_count,
        })






# ******************************************************************************
# ==============================================================================
# *** Admin Dashboard Stats ***
class AdminDashboardStatsView(generics.GenericAPIView):
    def get(self, request):
        users_count = models.User.objects.count()
        superuser_count = models.User.objects.filter(is_superuser=True, is_staff=True).count()
        admins_count = models.User.objects.filter(is_admin=True).count()
        teachers_count = models.User.objects.filter(is_teacher=True).count()
        staffs_count = models.User.objects.filter(is_superuser=False, is_staff=True).count()
        students_count = models.User.objects.filter(is_student=True).count()

        categories_section_count = models.CategorySection.objects.count()
        sections_course_count = models.SectionCourse.objects.count()

        courses_count = models.Course.objects.count()
        sections_in_course_count = models.SectionInCourse.objects.count()
        lessons_count = models.LessonInCourse.objects.count()

        coupons_course_count = models.CouponCourse.objects.count()
        
        total_enrolled_students = models.StudentCourseEnrollment.objects.count()

        questionbanks_count = models.QuestionBank.objects.count()

        if 'user_id' in request.GET:
            user_id = request.GET['user_id']
            if user_id[-1] == "/":
                user_id = user_id[:-1]
            user_id = int(user_id)
            admin_categories_section_count = models.CategorySection.objects.filter(user=user_id).count()
            admin_sections_course_count = models.SectionCourse.objects.filter(user=user_id).count()
            admin_courses_count = models.Course.objects.filter(user=user_id).count()
            admin_coupon_course_count = models.CouponCourse.objects.filter(user=user_id).count()
            admin_banks_count = models.QuestionBank.objects.filter(user=user_id).count()
        else:
            admin_categories_section_count = 0
            admin_sections_course_count = 0
            admin_courses_count = 0
            admin_coupon_course_count = 0
            admin_banks_count = 0

        contacts_count = models.ContactUsUser.objects.count()
        reviews_count = models.ReviewUser.objects.count()

        return Response({
            'users_count': users_count,
            'superuser_count': superuser_count,
            'admins_count': admins_count,
            'teachers_count': teachers_count,
            'staffs_count': staffs_count,
            'students_count': students_count,

            'categories_section_count': categories_section_count,
            'sections_course_count': sections_course_count,

            'courses_count': courses_count,
            'sections_in_course_count': sections_in_course_count,
            'lessons_count': lessons_count,
            
            'coupons_course_count': coupons_course_count,

            'total_enrolled_students': total_enrolled_students,

            'questionbanks_count': questionbanks_count,

            "admin_categories_section_count": admin_categories_section_count,
            "admin_sections_course_count": admin_sections_course_count,
            "admin_courses_count": admin_courses_count,
            "admin_coupon_course_count": admin_coupon_course_count,
            "admin_banks_count": admin_banks_count,

            'contacts_count': contacts_count,
            'reviews_count': reviews_count,
        })





# ******************************************************************************
# ==============================================================================
# *** Teacher Dashboard Stats ***
class TeacherDashboardStatsView(generics.GenericAPIView):
    def get(self, request):
        if 'user_id' in request.GET:
            user_id = request.GET['user_id']
            if user_id[-1] == "/":
                user_id = user_id[:-1]
            user_id = int(user_id)
            teacher_courses_count = models.Course.objects.filter(user=user_id).count()
            teacher_banks_count = models.QuestionBank.objects.filter(user=user_id).count()
        else:
            teacher_courses_count = 0
            teacher_banks_count = 0

        contacts_count = models.ContactUsUser.objects.count()
        reviews_count = models.ReviewUser.objects.count()

        return Response({
            "teacher_courses_count": teacher_courses_count,
            "teacher_banks_count": teacher_banks_count,

            'contacts_count': contacts_count,
            'reviews_count': reviews_count,
        })






# ******************************************************************************
# ==============================================================================
# *** Student Dashboard Stats ***
class StudentDashboardStatsView(generics.GenericAPIView):
    def get(self, request):
        if 'user_id' in request.GET:
            user_id = request.GET['user_id']
            if user_id[-1] == "/":
                user_id = user_id[:-1]
            user_id = int(user_id)

            # 
            student_courses_enrollment_count = models.StudentCourseEnrollment.objects.filter(student=user_id).count()
            student_favorite_course_count = models.StudentFavoriteCourse.objects.filter(student=user_id).count()

            # 
            student_questionbank_result_count = models.StudentQuestionBankResult.objects.filter(user=user_id).count()
        else:
            # 
            student_courses_enrollment_count = 0
            student_favorite_course_count = 0

            # 
            student_questionbank_result_count = 0

        return Response({
            # 
            "student_courses_enrollment_count": student_courses_enrollment_count,
            "student_favorite_course_count": student_favorite_course_count,

            # 
            "student_questionbank_result_count": student_questionbank_result_count,
 
        })






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
