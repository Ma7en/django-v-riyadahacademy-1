# 
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.flatpages.models import FlatPage
from django.db.models import Q


# 
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


# 
from cores import models
from cores import serializer

# Create your views here.

# ****************************************************************
# =================================================================
# *** Category Section ***
class CategorySectionList(generics.ListCreateAPIView):
    queryset = models.CategorySection.objects.all()
    serializer_class = serializer.CategorySectionSerializer

class CategorySectionPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CategorySection.objects.all()
    serializer_class = serializer.CategorySectionSerializer


# ****************************************************************
# =================================================================
# *** Section Course ***
class SectionCourseList(generics.ListCreateAPIView):
    queryset = models.SectionCourse.objects.all()
    serializer_class = serializer.SectionCourseSerializer

class SectionCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SectionCourse.objects.all()
    serializer_class = serializer.SectionCourseSerializer




# ****************************************************************
# =================================================================
# *** Course ***
class StandardResultSetPagination(PageNumberPagination):
    page_size=8
    page_size_query_param='page_size'
    max_page_size=1

class CourseList(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializer.CourseSerializer

class CoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializer.CourseSerializer

class CourseListAPI(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializer.CourseSerializer
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        qs=super().get_queryset()
        if 'result' in self.request.GET:
            limit=int(self.request.GET['result'])
            qs=models.Course.objects.all().order_by('-id')[:limit]
        if 'popular' in self.request.GET:
            qs=models.Course.objects.all().order_by('-id')[:limit]

        if 'category' in self.request.GET :
            category=self.request.GET['category']
            category=models.CourseCategory.objects.filter(id=category).first()
            qs=models.Course.objects.filter(category=category)

        if 'skill_name' in self.request.GET and 'teacher' in self.request.GET:
            skill_name=self.request.GET['skill_name']
            teacher=self.request.GET['teacher']
            teacher=models.Teacher.objects.filter(id=teacher).first()
            qs=models.Course.objects.filter(techs__icontains=skill_name,teacher=teacher)

        if 'searchstring' in self.kwargs:
            search=self.kwargs['searchstring']
            qs=models.Course.objects.filter(Q(title__icontains=search)|Q(title__icontains=search))
        
        return qs


class SectionList(generics.ListCreateAPIView):
    queryset = models.Section.objects.all()
    serializer_class = serializer.SectionSerializer

class SectionPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Section.objects.all()
    serializer_class = serializer.SectionSerializer



class ItemList(generics.ListCreateAPIView):
    queryset = models.Item.objects.all()
    serializer_class = serializer.ItemSerializer

class ItemPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Item.objects.all()
    serializer_class = serializer.ItemSerializer



class FileList(generics.ListCreateAPIView):
    queryset = models.File.objects.all()
    serializer_class = serializer.FileSerializer

class FilePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.File.objects.all()
    serializer_class = serializer.FileSerializer


    
class QuestionList(generics.ListCreateAPIView):
    queryset = models.Question.objects.all()
    serializer_class = serializer.QuestionSerializer

class QuestionPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Question.objects.all()
    serializer_class = serializer.QuestionSerializer


# ****************************************************************
# =================================================================
# *** Student Enroll Course ***
class StudentEnrollCourseList(generics.ListCreateAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = serializer.StudentCourseEnrollSerializer

class StudentEnrollCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = serializer.StudentCourseEnrollSerializer

def fetch_enroll_status(request,student_id,course_id):
    student = models.User.objects.filter(id=student_id).first()
    course = models.Course.objects.filter(id=course_id).first()
    enrollStatus = models.StudentCourseEnrollment.objects.filter(course=course,student=student).count()

    if enrollStatus:
        return JsonResponse({'bool':True})
    else:
        return JsonResponse({'bool':False})

class EnrolledStuentList(generics.ListAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = serializer.StudentCourseEnrollSerializer

    def get_queryset(self):
        if 'course_id' in self.kwargs:
            course_id=self.kwargs['course_id']
            course=models.Course.objects.get(pk=course_id)
            return models.StudentCourseEnrollment.objects.filter(course=course)
        
        elif 'teacher_id' in self.kwargs:
            teacher_id=self.kwargs['teacher_id']
            teacher=models.User.objects.get(pk=teacher_id)
            return models.StudentCourseEnrollment.objects.filter(course__teacher=teacher).distinct()
        
        elif 'student_id' in self.kwargs:
            student_id=self.kwargs['student_id']
            student=models.User.objects.get(pk=student_id)
            return models.StudentCourseEnrollment.objects.filter(student=student).distinct()
        
        elif 'studentId' in self.kwargs:
            student_id=self.kwargs['student_id']
            student=models.User.objects.get(pk=student_id)
            print(student.interseted_categories)
            queries=[Q(techs__iendwith=value) for value in student.interseted_categories]
            query=queries.pop()
            for item in queries:
                query |= item
            qs=models.Course.objects.filter(query)

        return qs


class EnrolledStuentPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.StudentCourseEnrollment.objects.all()
    serializer_class = serializer.StudentCourseEnrollSerializer



# ****************************************************************
# =================================================================
# *** Course Rating ***
class CourseRatingList(generics.ListCreateAPIView):
    queryset = models.CourseRating.objects.all()
    serializer_class = serializer.CourseRatingSerializer
    pagination_class = StandardResultSetPagination

    def get_queryset(self):
        if 'popular' in self.request.GET:
            sql="SELECT *, AVG(cr.rating) as avg_rating FROM main_courserating as cr INNER JOIN main_course as c ON cr.course_id=c.id GROUP BY c.id ORDER BY avg_rating desc LIMIT 3"
            return models.CourseRating.objects.raw(sql)
        
        if 'all' in self.request.GET:
            sql="SELECT *, AVG(cr.rating) as avg_rating FROM main_courserating as cr INNER JOIN main_course as c ON cr.course_id=c.id GROUP BY c.id ORDER BY avg_rating desc"
            return models.CourseRating.objects.raw(sql)
        
        return models.CourseRating.objects.filter(course__isnull=False).order_by('-rating')


class CourseRatingPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CourseRating.objects.all()
    serializer_class = serializer.CourseRatingSerializer


def fetch_rating_status(request,student_id,course_id):
    student=models.User.objects.filter(id=student_id).first()
    course=models.Course.objects.filter(id=course_id).first()
    ratingStatus=models.CourseRating.objects.filter(course=course,student=student).count()

    if ratingStatus:
        return JsonResponse({'bool':True})
    else:
        return JsonResponse({'bool':False})





# ****************************************************************
# =================================================================
# *** Student Favorite Course ***
class StudentFavoriteCourseList(generics.ListCreateAPIView):
    queryset = models.StudentFavoriteCourse.objects.all()
    serializer_class = serializer.StudentFavoriteCourseSerializer

    def get_queryset(self):
        if 'student_id' in self.kwargs:
            student_id=self.kwargs['student_id']
            student=models.User.objects.get(pk=student_id)
            return models.StudentFavoriteCourse.objects.filter(student=student).distinct()

class StudentFavoriteCoursePK(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.StudentFavoriteCourse.objects.all()
    serializer_class = serializer.StudentFavoriteCourseSerializer


def remove_favorite_course(request,course_id,student_id):
    student=models.User.objects.filter(id=student_id).first()
    course=models.Course.objects.filter(id=course_id).first()
    favoriteStatus=models.StudentFavoriteCourse.objects.filter(course=course,student=student).delete()

    if favoriteStatus:
        return JsonResponse({'bool':True})
    else:
        return JsonResponse({'bool':False})



# ****************************************************************
# =================================================================
# ***  ***



# ****************************************************************
# =================================================================
# ***  ***



# ****************************************************************
# =================================================================
# ***  ***



# ****************************************************************
# =================================================================
# ***  ***



# ****************************************************************
# =================================================================
# ***  ***



# ****************************************************************
# =================================================================
# ***  ***



# ****************************************************************
# =================================================================
# ***  ***



# ****************************************************************
# =================================================================
# ***  ***



# ****************************************************************
# =================================================================
# ***  ***



# ****************************************************************
# =================================================================
# ***  ***



# ****************************************************************
# =================================================================
# *** Teacher Student Chat ***
@csrf_exempt
def ChatBot(request,teacher_id,student_id):
    teacher = models.User.objects.get(id=teacher_id)
    student = models.User.objects.get(id=student_id)
    msg_to = request.POST.get('msg_to')
    msg_from = request.POST.get('msg_from')
    msgRes = models.TeacherStudentChat.objects.create(
        teacher=teacher,
        student=student,
        msg_to=msg_to,
        msg_from=msg_from
    )

    if msgRes:
        return JsonResponse({'bool':True,'msg':'Message sended'})
    else:
        return JsonResponse({'bool':False,'msg':'Message failed'})

class MessageList(generics.ListAPIView):
    queryset = models.TeacherStudentChat.objects.all()
    serializer_class = serializer.TeacherStudentChatSerializer

    def get_queryset(self):
        teacher_id=self.kwargs['teacher_id']
        student_id=self.kwargs['student_id']
        teacher=models.User.objects.get(pk=teacher_id)
        student=models.User.objects.get(pk=student_id)
        return models.TeacherStudentChat.objects.filter(teacher=teacher,student=student).exclude(msg_to='')

@csrf_exempt
def GroupChatBot(request,teacher_id):
    teacher = models.User.objects.get(id=teacher_id)
    msg_to = request.POST.get('msg_to')
    msg_from = request.POST.get('msg_from')
    enrolledList = models.StudentCourseEnrollment.objects.filter(course__teacher=teacher).distinct()
    
    for enrolled in enrolledList:
        msgRes = models.TeacherStudentChat.objects.create(
            teacher=teacher,
            student=enrolled.student,
            msg_to=msg_to,
            msg_from=msg_from
        )

    if msgRes:
        return JsonResponse({'bool':True,'msg':'Message sended'})
    else:
        return JsonResponse({'bool':False,'msg':'Message failed'})



# ****************************************************************
# =================================================================
# *** ContactUs ***
# (List of contact us -> [GET, POST])
class ContactUsListAPIView(generics.ListCreateAPIView):
    queryset = models.ContactUsUser.objects.all()
    serializer_class = serializer.ContactUsUserSerializer

# (List of contact us -> [GET, POST, PUT, DELETE])
class ContactUsPKAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ContactUsUser.objects.all()
    serializer_class = serializer.ContactUsUserSerializer


# ****************************************************************
# =================================================================
# *** Review ***
# (List of review -> [GET, POST])
class ReviewUserListAPIView(generics.ListCreateAPIView):
    queryset = models.ReviewUser.objects.all()
    serializer_class = serializer.ReviewUserSerializer

# (List of review -> [GET, POST, PUT, DELETE])
class ReviewUserPKAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ReviewUser.objects.all()
    serializer_class = serializer.ReviewUserSerializer


# ****************************************************************
# =================================================================
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

# ****************************************************************
# =================================================================
# ***  ***