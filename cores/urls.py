from django.urls import path, include
from django.urls import path, include



#
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers



#
from . import views




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

    path(
        'category-section/search/<str:searchstring>/', 
        views.CategorySectionSearchList.as_view(),
        name="category-section-search-list",
    ),



    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
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

    # (Category)
    path(
        "section-course/category/<int:pk>/",
        views.SectionCourseCategoryList.as_view(),
        name="section-course-category-pk",
    ),
    
    path(
        'section-course/search/<str:searchstring>/', 
        views.SectionCourseSearchList.as_view(),
        name="section-course-search-list",
    ),



    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
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
        'courses/search/<str:searchstring>/', 
        views.CourseListAPI.as_view(),
        name="course-list-search",
    ),


    # Course URLs
    path(
        'courses/', 
        views.CourseListCreate.as_view(), 
        name='course-list',
    ),
    path(
        'courses/<int:pk>/', 
        views.CourseRetrieveUpdateDestroy.as_view(), 
        name='course-detail',
    ),
    path(
        'public/courses/', 
        views.PublicCourseList.as_view(), 
        name='public-course-list',
    ),

        
    # path(
    #     'courses/search/<str:searchstring>/', 
    #     views.CoursesSearchList.as_view(),
    #     name="courses-search-list",
    # ),

   

    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ), 
    # Section In Course URLs (nested under courses)
    path(
        'courses/sections/list/', 
        views.SectionInCourseList.as_view(), 
        name='sections-in-course-list',
    ),
    path(
        'courses/sections/<int:pk>/', 
        views.SectionInCoursePK.as_view(), 
        name='section-in-course-pk',
    ),

    path(
        'courses/<int:course_id>/sections/', 
        views.SectionInCourseListCreate.as_view(), 
        name='section-in-course-list',
    ),
    path(
        'courses/<int:course_id>/sections/<int:pk>/', 
        views.SectionInCourseRetrieveUpdateDestroy.as_view(), 
        name='section-in-course-detail',
    ),

   


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ), 
    # Lesson In Course URLs (nested under sections)
    path(
        'courses/sections/lessons/list/',
        views.LessonInCourseList.as_view(), 
        name='lesson-in-course-list',
    ),
    path(
        'courses/sections/lessons/<int:pk>/',
        views.LessonInCoursePK.as_view(), 
        name='lesson-in-course-pk',
    ),

    path(
        'courses/sections/list/<int:section_id>/lessons/', 
        views.LessonInCourseListCreate.as_view(), 
        name='lesson-list',
    ),

    path(
        'courses/sections/<int:section_id>/lessons/<int:pk>/', 
        views.LessonInCourseRetrieveUpdateDestroy.as_view(), 
        name='lesson-detail',
    ),
    path(
        'courses/sections/<int:section_id>/lessons/', 
        views.LessonInCourseCreateView.as_view(), 
        name='lesson-create',
    ),


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # File In Course URLs (nested under lessons)
    path(
        'courses/sections/lessons/files/list/', 
        views.FileInCourseList.as_view(), 
        name='lesson-file-in-course-list',
    ),
    path(
        'courses/sections/lessons/files/<int:pk>/', 
        views.FileInCoursePK.as_view(), 
        name='lesson-file-in-course-pk',
    ),

    path(
        'courses/sections/lessons/list/<int:lesson_id>/files/', 
        views.FileInCourseListCreate.as_view(), 
        name='lesson-file-list',
    ),

    path(
        'courses/sections/lessons/<int:lesson_id>/files/<int:pk>/', 
        views.FileInCourseRetrieveUpdateDestroy.as_view(), 
        name='lesson-file-detail',
    ),
    path(
        'courses/sections/lessons/<int:lesson_id>/files/', 
        views.FileInCourseCreateView.as_view(), 
        name='lesson-file-create',
    ),

    
    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # Question In Course URLs (nested under lessons)
    path(
        'courses/sections/lessons/questions/list/', 
        views.QuestionInCourseList.as_view(), 
        name='question-in-cours-list',
    ),
    path(
        'courses/sections/lessons/questions/<int:pk>/', 
        views.QuestionInCoursePK.as_view(), 
        name='question-in-cours-pk',
    ),

    path(
        'courses/sections/lessons/list/<int:lesson_id>/questions/', 
        views.QuestionInCourseListCreate.as_view(), 
        name='question-list',
    ),

    path(
        'courses/sections/lessons/<int:lesson_id>/questions/<int:pk>/', 
        views.QuestionInCourseRetrieveUpdateDestroy.as_view(), 
        name='question-detail',
    ),
    path(
        'courses/sections/lessons/<int:lesson_id>/questions/', 
        views.QuestionCreateView.as_view(), 
        name='question-create',
    ),



    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # (Section)
    path(
        "course/section-course/<int:pk>/",
        views.CourseSectionList.as_view(),
        name="course-section-course-pk",
    ),
    
    # =================================================================
    # ***  *** #
    # path('courses/', include(router.urls)),


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # =================================================================
    # *** Coupon Course *** #
    path(
        "coupon-course/list/",
        views.CouponCourseList.as_view(),
        name="coupon-course-list",
    ),
    path(
        "coupon-course/<int:pk>/",
        views.CouponCoursePK.as_view(),
        name="coupon-course-pk",
    ),


    path(
        "coupon-course/<str:searchstring>/",
        views.CouponCourseSearch.as_view(),
        name="coupon-course-search",
    ),
    


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # =================================================================
    # *** Course Payment Checkout *** #
    path(
        'create-checkout/', 
        views.CourseCreateCheckoutView.as_view(), 
        name='create-checkout',
    ),
    path(
        'payment-result/', 
        views.CoursePaymentResultView.as_view(), 
        name='payment-result',
    ),



    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
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



    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
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

        
    # path(
    #     'course-rating/search/<str:searchstring>/', 
    #     views.CourseRatingSearchList.as_view(),
    #     name="courses-rating-search-list",
    # ),



    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
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

    
    # path(
    #     'student-favorite-course/search/<str:searchstring>/', 
    #     views.StudentFavoriteCourseSearchList.as_view(),
    #     name="student-favorite-course-search-list",
    # ),



    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
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


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # ================================================================
    # *** ) Student Progress Course *** #
    path(
        'track-progress/<int:lesson_id>/', 
        views.TrackLessonProgressView.as_view(), 
        name='track-progress',
    ),
    path(
        'user-progress/', 
        views.GetUserProgressView.as_view(), 
        name='user-progress',
    ),


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # ================================================================
    # *** ) Student Certificate *** #
    path(
        'certificate/<int:enrollment_id>/', 
        views.student_generate_certificate, 
        name='generate_certificate',
    ),

    path(
        'certificates/generate/<int:course_id>/', 
        views.StudentGenerateCertificateView.as_view(), 
        name='generate-certificate'
    ),
    path(
        'certificates/my-certificates/', 
        views.StudentCertificatesView.as_view(), 
        name='user-certificates'
    ),
    path(
        'certificates/verify/<str:verification_code>/', 
        views.StudentVerifyCertificateView.as_view(), 
        name='verify-certificate'
    ),


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
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

    path(
        'quiz-results/save/<int:question_bank_id>/',
        views.StudentQuestionBankResultSaveView.as_view(),
        name='save-QuestionBank-results'
    ),

    # path(
    #     'question-bank/search/<str:searchstring>/', 
    #     views.QuestionBankSearchList.as_view(),
    #     name="question-bank-search-list",
    # ),



    
    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # (Section)
    path(
        "question-bank/section-course/<int:pk>/",
        views.QuestionBankSectionList.as_view(),
        name="question-bank-section-course-pk",
    ),
    

    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
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

    path(
        'contactus-user/search/<str:searchstring>/', 
        views.ContactusUserSearchList.as_view(),
        name="contactus-user-search-list",
    ),



    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
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
    
    # path(
    #     'review-user/search/<str:searchstring>/', 
    #     views.ReviewUserSearchList.as_view(),
    #     name="review-user-search-list",
    # ),



    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
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
