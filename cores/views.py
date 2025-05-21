# 
from django.shortcuts import render


# 
from rest_framework import generics
from rest_framework.response import Response


# 
from cores import models
from cores import serializer


# Create your views here.
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