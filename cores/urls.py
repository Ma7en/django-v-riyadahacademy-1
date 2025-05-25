from django.urls import path, include
from django.urls import path, include


#
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

#
from cores import views

# =================================================================
# 
# router = DefaultRouter()
# router.register(r'', views.CourseViewSet)
# router.register(r'sections', views.SectionViewSet)
# router.register(r'items', views.ItemViewSet)
# router.register(r'files', views.FileViewSet)
# router.register(r'questions', views.QuestionViewSet)

# =================================================================
# 
# router = routers.DefaultRouter()
# router.register(r'courses', views.CourseViewSet)

# # Nested routers for course sections
# courses_router = routers.NestedSimpleRouter(router, r'courses', lookup='course')
# courses_router.register(r'sections', views.SectionViewSet, basename='course-sections')

# # Nested routers for section items
# sections_router = routers.NestedSimpleRouter(courses_router, r'sections', lookup='section')
# sections_router.register(r'items', views.ItemViewSet, basename='section-items')

# # Nested routers for item files
# items_router = routers.NestedSimpleRouter(sections_router, r'items', lookup='item')
# items_router.register(r'files', views.FileViewSet, basename='item-files')
 
# # Nested routers for files
# items_router = routers.NestedSimpleRouter(sections_router, r'files', lookup='files')
# items_router.register(r'questions', views.FileViewSet, basename='questions')
 
# # Nested routers for questions
# questions_router = routers.NestedSimpleRouter(sections_router, r'questions', lookup='questions')
# # questions_router.register(r'files', views.FileViewSet, basename='item-files')



# =================================================================
questionbank = DefaultRouter() 
questionbank.register(r'', views.QuestionBankViewSet)
questionbank.register(r'questions', views.QuestionInBankViewSet)



urlpatterns = [
    # =================================================================
    # *** Category Section *** #
    path(
        "category-section/list/",
        views.CategorySectionList.as_view(),
        name="category-section-list",
    ),
    path(
        "category-section/<int:pk>/",
        views.CategorySectionPK.as_view(),
        name="category-section-pk",
    ),

    # =================================================================
    # *** Section Course *** #
    path(
        "section-course/list/",
        views.SectionCourseList.as_view(),
        name="section-course-list",
    ),
    path(
        "section-course/<int:pk>/",
        views.SectionCoursePK.as_view(),
        name="section-course-pk",
    ),
    
    # =================================================================
    # *** Course *** #
    path(
        "course/list/",
        views.CourseList.as_view(),
        name="course-list",
    ),
    path(
        "course/<int:pk>/",
        views.CoursePK.as_view(),
        name="course-pk",
    ),
    
    path(
        "course/",
        views.CourseListAPI.as_view(),
        name="course-list-api",
    ),
    path(
        'search-courses/<str:searchstring>/', 
        views.CourseList.as_view(),
        name="course-list-search",
    ),
    
    # =================================================================
    # ***  *** #
    # path('courses/', include(router.urls)),

    # =================================================================
    # *** Student Enroll Course *** #
    path(
        'student-enroll-course/list/', 
        views.StudentEnrollCourseList.as_view(),
        name="student-enroll-course-list",
    ),
    path(
        'student-enroll-course/<int:pk>/', 
        views.StudentEnrollCoursePK.as_view(),
        name="student-enroll-course-pk",
    ),

    path(
        'student-enroll-course/', 
        views.StudentEnrollCourseList.as_view(),
        name="student-enroll-course",
    ),
    
    path(
        'fetch-enroll-status/<int:student_id>/<int:course_id>/', 
        views.fetch_enroll_status,
        name="fetch-enroll-status-student_id-course_id",
    ),

    path(
        'fetch-enrolled-students/<int:course_id>/', 
        views.EnrolledStuentList.as_view(),
        name="fetch-enrolled-students-course_id",
    ),

    path(
        'fetch-all-enrolled-students/<int:teacher_id>/', 
        views.EnrolledStuentList.as_view(),
        name="fetch-all-enrolled-students-teacher_id",
    ),

    path(
        'fetch-enrolled-courses/<int:student_id>/', 
        views.EnrolledStuentList.as_view(),
        name="fetch-enrolled-courses-student_id",
    ),

    path(
        'fetch-recomemded-coourses/<int:student_id>/', 
        views.EnrolledStuentList.as_view(),
        name="fetch-recomemded-coourses-student_id",
    ),



    # =================================================================
    # *** Course Rating *** #
    path(
        'course-rating/list/', 
        views.CourseRatingList.as_view(),
        name="course-rating-list",
    ),
    path(
        'course-rating/<int:pk>/', 
        views.CourseRatingPK.as_view(),
        name="course-rating-pk",
    ),


    path(
        'course-rating/', 
        views.CourseRatingListAPI.as_view(),
        name="course-rating",
    ),
    path(
        'popular-courses/', 
        views.CourseRatingListAPI.as_view(),
        name="popular-courses",
    ),

    path(
        'fetch-rating-status/<int:student_id>/<int:course_id>/', 
        views.fetch_rating_status,
        name="fetch-rating-status-student_id-course_id",
    ),



    # =================================================================
    # *** Student Favorite Course *** #
    path(
        'student-add-favorte-course/list/', 
        views.StudentFavoriteCourseList.as_view(),
        name="student-add-favorte-course-list",
    ),
    path(
        'student-favorite-coourses/<int:pk>/', 
        views.StudentFavoriteCoursePK.as_view(),
        name="student-favorite-coourses-pk",
    ),

    path(
        'student-add-favorte-course/', 
        views.StudentFavoriteCourseListAPI.as_view(),
        name="student-add-favorte-course-list",
    ),
    path(
        'fetch-favorite-coourses/<int:student_id>/', 
        views.StudentFavoriteCourseListAPI.as_view(),
        name="fetch-favorite-coourses-student_id",
    ),

    path(
        'student-remove-favorite-course/<int:course_id>/<int:student_id>/', 
        views.remove_favorite_course,
        name="student-remove-favorite-course-course_id-student_id",
    ),

    # =================================================================
    # *** Teacher Student Chat *** #
    path(
        'get-message-teacher-student-chat/list/', 
        views.TeacherStudentChatList.as_view(), 
        name="message-List-teacher-student-chat",
    ),
    path(
        'get-message-teacher-student-chat/<int:pk>/', 
        views.TeacherStudentChatPK.as_view(), 
        name="message-details-pk",
    ),


    path(
        'send-message-teacher-student-chat/<int:teacher_id>/<int:student_id>/', 
        views.TeacherStudentChatBot, 
        name="Chat-Bot",
    ),

    path(
        'get-message-teacher-student-chat/<int:teacher_id>/<int:student_id>/', 
        views.TeacherStudentChatListAPI.as_view(), 
        name="Message-List",
    ),

    path(
        'send-group-message-teacher-student-chat/<int:teacher_id>/', 
        views.GroupTeacherStudentChatBot, 
        name="Group-Chat-Bot",
    ),

    # ================================================================
    # *** ) Questions Banks *** #
    path(
        'question-bank/list/',
        views.QuestionBankList.as_view(), 
        name="Question-Bank-List",  
    ),
    path(
        'question-bank/<int:pk>/',  
        views.QuestionBankPK.as_view(), 
        name="Question-Bank-PK",
    ),

    path('question-bank/', include(questionbank.urls)),
    path(
        'question-bank/results/<int:question_bank_id>/', 
        views.QuestionBankResultView.as_view(), 
        name='quiz-results',
    ),

    # ================================================================
    # *** 1) ContactUs *** #
    path(
        "contactus-user/list/",
        views.ContactUsListAPIView.as_view(),
        name="contactus-list",
    ),
    path(
        "contactus-user/<int:pk>/",
        views.ContactUsPKAPIView.as_view(),
        name="contactus-details-pk",
    ),

    # ================================================================
    # *** 2) Review *** #
    path(
        "review-user/list/",
        views.ReviewUserListAPIView.as_view(),
        name="review-user-list",
    ),
    path(
        "review-user/<int:pk>/",
        views.ReviewUserPKAPIView.as_view(),
        name="review-user-details-pk",
    ),
    
    # =================================================================
    # *** 2) Review *** #
    # path('category/', views.CategoryListView.as_view(), name='category-list',),
    # path('category/<int:pk>/', views.CategoryPkAPIView.as_view(), name='category-pk',),

    # path('posts/', views.PostListView.as_view(), name='post-list',),
    # path('comments/', views.CommentListView.as_view(), name='comment-list',),
    # path('replies/', views.ReplyListView.as_view(), name='reply-list',),
    # path('notifications/', views.NotificationListView.as_view(), name='notification-list',),
    # path('reports/', views.ReportListView.as_view(), name='report-list',),

    # =================================================================
]
