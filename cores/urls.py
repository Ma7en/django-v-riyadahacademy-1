# 
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
# questionbank.register(r'', views.QuestionBankViewSet)
# questionbank.register(r'', views.QuestionInBankViewSet)



urlpatterns = [
    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # =================================================================
    # *** Category Section *** #
    # (List)
    path(
        "startapp/list/",
        views.StartappList.as_view(),
        name="startapp-list",
    ),
    # (List App)
    path(
        "startapp/list-app/",
        views.StartappListApp.as_view(),
        name="startapp-list-app",
    ),
    # (List App)
    path(
        "startapp/list-admin/",
        views.StartappListAdmin.as_view(),
        name="startapp-list-admin",
    ),
    # (List Result)
    path(
        "startapp/result/", #?result=9
        views.StartappResultList.as_view(),
        name="course-result-list",
    ),
    # (PK)
    path(
        "startapp/<int:pk>/",
        views.StartappPK.as_view(),
        name="startapp-pk",
    ),
    # (Search)
    path(
        'startapp/search/<str:searchstring>/', 
        views.StartappSearchList.as_view(),
        name="startapp-search-list",
    ),


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # =================================================================
    # *** Category Section *** #
    # (List)
    path(
        "category-section/list/",
        views.CategorySectionList.as_view(),
        name="category-section-list",
    ),
    # (List App)
    path(
        "category-section/list-app/",
        views.CategorySectionListApp.as_view(),
        name="category-section-list",
    ),
    # (List App Ordered )
    path(
        "category-section/list-app-ordered/",
        views.CategorySectionListAppOrdered.as_view(),
        name="category-section-list",
    ),
    # (List Admin)
    path(
        "category-section/list-admin/",
        views.CategorySectionListAdmin.as_view(),
        name="category-section-list",
    ),
    # (List Result)
    path(
        "category-section/result/", #?result=9
        views.CategorySectionResultList.as_view(),
        name="course-result-list",
    ),
    # (PK)
    path(
        "category-section/<int:pk>/",
        views.CategorySectionPK.as_view(),
        name="category-section-pk",
    ),
    # (Search)
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
    # (List)
    path(
        "section-course/list/",
        views.SectionCourseList.as_view(),
        name="section-course-list",
    ),
    # (List App)
    path(
        "section-course/list-app/",
        views.SectionCourseListApp.as_view(),
        name="section-course-list",
    ),
    # (List Admin)
    path(
        "section-course/list-admin/",
        views.SectionCourseListAdmin.as_view(),
        name="section-course-list",
    ),
    # (List Result)
    path(
        "section-course/result/", #?result=9
        views.SectionCourseResultList.as_view(),
        name="course-result-list",
    ),
    # (PK)
    path(
        "section-course/<int:pk>/",
        views.SectionCoursePK.as_view(),
        name="section-course-pk",
    ),
    # (Search)
    path(
        'section-course/search/<str:searchstring>/', 
        views.SectionCourseSearchList.as_view(),
        name="section-course-search-list",
    ),



    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # +++
    path(
        "section-course/category/list/",
        views.SectionCourseCategoriesList.as_view(),
        name="section-course-list",
    ),
    # (Category PK)
    path(
        "section-course/category/<int:pk>/",
        views.SectionCourseCategoryList.as_view(),
        name="section-course-category-pk",
    ),



    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # =================================================================
    # *** Course *** #
    # (List)
    path(
        "course/list/",
        views.CourseList.as_view(),
        name="course-list",
    ),
    # (List App)
    path(
        "course/list-app/",
        views.CourseListApp.as_view(),
        name="course-list",
    ),
    # (List Admin)
    path(
        "course/list-admin/",
        views.CourseListAdmin.as_view(),
        name="course-list",
    ),
    # (List Result)
    path(
        "course/result/", #?result=9
        views.CourseResultList.as_view(),
        name="course-result-list",
    ),
    # (PK)
    path(
        "course/<int:pk>/",
        views.CoursePK.as_view(),
        name="course-pk",
    ),
    # (All PK)
    path(
        "course/all/<int:pk>/",
        views.CourseDetailAll.as_view(),
        name="course-all-pk",
    ),
    # +++
    path(
        "course/",
        views.CourseListAPI.as_view(),
        name="course-list-api",
    ),
    # +++
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
    # +++
    path(
        'courses/<int:pk>/', 
        views.CourseRetrieveUpdateDestroy.as_view(), 
        name='course-detail',
    ),
    # +++
    path(
        'public/courses/', 
        views.PublicCourseList.as_view(), 
        name='public-course-list',
    ),
    # (Search)
    path(
        'courses/search/<str:searchstring>/', 
        views.CoursesSearchList.as_view(),
        name="courses-search-list",
    ),

   


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # *** Course Not All *** #
    # (List)
    path(
        "course-not-all/list/",
        views.CourseNotAllList.as_view(),
        name="course-not-all-list",
    ),
    # (List App)
    path(
        "course-not-all/list-app/",
        views.CourseNotAllListApp.as_view(),
        name="course-not-all-list-app",
    ),

    # (List Admin)
    path(
        "course-not-all/list-admin/",
        views.CourseNotAllListAdmin.as_view(),
        name="course-not-all-list-admin",
    ),
   
    # (List Result)
    path(
        "course-not-all/result/", #?result=9
        views.CourseNotAllResultList.as_view(),
        name="course-not-all-result-list",
    ),

    # (PK)
    path(
        "course-and-section-in-course/<int:pk>/",
        views.CourseAndSectionInCoursePK.as_view(),
        name="course-and-section-in-course-pk",
    ),

    # (All PK)
    path(
        "course-not-all/all/<int:pk>/",
        views.CourseDetailAll.as_view(),
        name="course-not-all-all-pk",
    ),


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # (Section PK)
    path(
        "course/section-course/<int:pk>/",
        views.CourseSectionCourseList.as_view(),
        name="course-section-course-pk",
    ),



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
    # (PK)
    path(
        'courses/sections/<int:pk>/', 
        views.SectionInCoursePK.as_view(), 
        name='section-in-course-pk',
    ),
    # ()
    path(
        'courses/<int:course_id>/sections/', 
        views.SectionInCourseListCreate.as_view(), 
        name='section-in-course-list',
    ),
    # 
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
        'courses/sections/<int:section_id>/lessons/', 
        views.LessonInCourseListCreate.as_view(), 
        name='lesson-list',
    ),

    path(
        'courses/sections/<int:section_id>/lessons/<int:pk>/', 
        views.LessonInCourseRetrieveUpdateDestroy.as_view(), 
        name='lesson-detail',
    ),
    path(
        'courses/sections/list/<int:section_id>/lessons/', 
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


    
    # =================================================================
    # ***  *** #
    # path('courses/', include(router.urls)),


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # =================================================================
    # *** Coupon Course *** #
    # (List)
    path(
        "coupon-course/list/",
        views.CouponCourseList.as_view(),
        name="coupon-course-list",
    ),
    # (List App)
    path(
        "coupon-course/list-app/",
        views.CouponCourseListApp.as_view(),
        name="coupon-course-list",
    ),
    # (PK)
    path(
        "coupon-course/<int:pk>/",
        views.CouponCoursePK.as_view(),
        name="coupon-course-pk",
    ),
    # (Search)
    path(
        "coupon-course/search/<str:searchstring>/",
        views.CouponCourseSearch.as_view(),
        name="coupon-course-search",
    ),
    # (Search App)
    path(
        "coupon-course/search-app/<str:searchstring>/",
        views.CouponCourseSearchApp.as_view(),
        name="coupon-course-search",
    ),
    # (Search App)
    path(
        "coupon-course/search-app-usage/<str:searchstring>/",
        views.CouponCourseSearchAppUsage.as_view(),
        name="coupon-course-search",
    ),
    # (Increment Usage)
    path(
        'coupon-course/increment/<str:name>/',
        views.CouponCourseIncrementUsageView.as_view(),
        name='coupon-course-increment-usage'
    ),



    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # =================================================================
    # *** Course Payment Checkout *** #
    # (checkout)
    path(
        'create-checkout/', 
        views.CourseCreateCheckoutView.as_view(), 
        name='create-checkout',
    ),
    # (payment)
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
        # views.fetch_enroll_status,
        views.FetchEnrollStatusView.as_view(),
        name="fetch-enroll-status-student_id-course_id",
    ),

    #- 
    path(
        'fetch-enrolled-students/<int:course_id>/', 
        views.EnrolledStuentCourseList.as_view(),
        name="fetch-enrolled-students-course_id",
    ),

    path(
        'fetch-all-enrolled-students/<int:teacher_id>/', 
        views.EnrolledAllStuentList.as_view(),
        name="fetch-all-enrolled-students-teacher_id",
    ),

    # user enrolled course()
    path(
        'fetch-enrolled-courses/<int:student_id>/', 
        views.EnrolledStuentPkList.as_view(),
        name="fetch-enrolled-courses-student_id",
    ),


    path(
        'fetch-recomemded-courses/<int:student_id>/', 
        views.EnrolledRecomemdedStuentList.as_view(),
        name="fetch-recomemded-courses-student_id",
    ),

    

    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # user enrolled course (not all)
    path(
        'fetch-enrolled-courses-not-all/<int:student_id>/', 
        views.EnrolledStuentCoursesNotaAllPkList.as_view(),
        name="fetch-enrolled-courses-nota-all-student_id",
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
        'popular-courses-rating/', 
        views.CourseRatingListAPI.as_view(),
        name="popular-courses",
    ),

    path(
        'fetch-rating-status/<int:student_id>/<int:course_id>/',
        # views.fetch_rating_status, 
        views.FetchRatingStatusView.as_view(),
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
        # views.remove_favorite_course,
        views.RemoveFavoriteCourseView.as_view(),
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


    # path(
    #     'send-message-teacher-student-chat/<int:teacher_id>/<int:student_id>/', 
    #     views.TeacherStudentChatBot, 
    #     name="Chat-Bot",
    # ),
    path(
        'send-message-teacher-student-chat/<int:teacher_id>/<int:student_id>/', 
        views.TeacherStudentChatBot.as_view(), 
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
        'get-message-teacher-chat/<int:teacher_id>/', 
        views.TeacherAllChatListAPI.as_view(), 
        name="teacher-Message-List",
    ),

    path(
        'teacher-student-chats/', 
        views.TeacherStudentChatListView.as_view(), 
        name='teacher-student-chat-list',
    ),
    path(
        'teacher-student-chats/<int:teacher_id>/', 
        views.TeacherSpecificStudentsListView.as_view(), 
        name='teacher-specific-students-list',
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
     # =================================================================
    # *** 7) Subscribe Course *** #
    # (List) 
    path(
        'subscribe-course/list/', 
        views.SubscribeCourseList.as_view(), 
        name='subscribe-course-list',
    ),
    # (List App)
    path(
        'subscribe-course/list-app/', 
        views.SubscribeCourseListApp.as_view(), 
        name='subscribe-course-list-app',
    ),
    # (List Admin)
    path(
        'subscribe-course/list-admin/', 
        views.SubscribeCourseListAdmin.as_view(), 
        name='subscribe-course-list-admin',
    ),
    # (List Result)
    path(
        'subscribe-course/result/',  #?result=9
        views.SubscribeCourseResultList.as_view(), 
        name='subscribe-course-result-list',
    ),
    # (PK)
    path(
        'subscribe-course/<int:pk>/', 
        views.SubscribeCoursePK.as_view(), 
        name='subscribe-course-pk',
    ),
    # (Search)
    path(
        'subscribe-courses/search/<str:searchstring>/', 
        views.SubscribeCoursesSearchList.as_view(),
        name="subscribe-courses-search-list",
    ),


  


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # ================================================================
    # *** ) Document *** #
    # (List)
    path(
        'document/list/', 
        views.DocumentList.as_view(), 
        name='Document-list',
    ),
    # (List Admin)
    path(
        'document/list-admin/', 
        views.DocumentListAdmin.as_view(), 
        name='Document-list-admin',
    ),
    # (List App)
    path(
        'document/list-app/', 
        views.DocumentListApp.as_view(), 
        name='Document-list-app',
    ),
    # (List Result)
    path(
        "document/result/", #?result=9
        views.DocumentResultList.as_view(),
        name="document-result-list",
    ),
    # (PK)
    path(
        'document/<int:pk>/', 
        views.DocumentPK.as_view(), 
        name='Document-detail',
    ),
    # (Search)
    path(
        'document/search/<str:searchstring>/', 
        views.DocumentSearchList.as_view(),
        name="document-search-list",
    ),

    # Document files endpoints
    path(
        'document/<int:document_id>/files/', 
        views.DocumentFileList.as_view(), 
        name='document-file-list',
    ),
    path(
        'document/file/<int:pk>/', 
        views.DocumentFileDetail.as_view(), 
        name='document-file-detail',
    ),


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # ================================================================
    # (Pk Section)
    path(
        "document/section-course/<int:pk>/",
        views.DocumentSectionList.as_view(),
        name="document-section-course-pk",
    ),
  


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # ================================================================
    # *** ) Questions Banks *** #
    # (List)
    path(
        'question-bank/list/', 
        views.QuestionBankList.as_view(), 
        name='questionbank-list',
    ),
    # (List Admin)
    path(
        'question-bank/list-admin/', 
        views.QuestionBankListAdmin.as_view(), 
        name='questionbank-list',
    ),
    # (List App)
    path(
        'question-bank/list-app/', 
        views.QuestionBankListApp.as_view(), 
        name='questionbank-list',
    ),
    # (List Result)
    path(
        "question-bank/result/", #?result=9
        views.QuestionBankResultList.as_view(),
        name="course-result-list",
    ),
    # (PK)
    path(
        'question-bank/<int:pk>/', 
        views.QuestionBankRetrieveUpdateDestroyView.as_view(), 
        name='questionbank-detail',
    ),
    
    
    

    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # (Search)
    path(
        'question-bank/search/<str:searchstring>/', 
        views.QuestionBankSearchList.as_view(),
        name="question-bank-search-list",
    ),    
    # (Pk Section)
    path(
        "question-bank/section-course/<int:pk>/",
        views.QuestionBankSectionList.as_view(),
        name="question-bank-section-course-pk",
    ),
    



    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # Get all questions for a specific bank
    # (Questions)
    path(
        'question-bank/<int:bank_id>/questions/', 
        views.BankQuestionsListView.as_view(), 
        name='bank-questions-list',
    ),



    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # *** ) Question In Banks *** #
    # (List)
    path(
        'question-bank/questions/list/', 
        views.QuestionListCreate.as_view(), 
        name='question-list',
    ),
    # (Pk)
    path(
        'question-bank/questions/<int:pk>/', 
        views.QuestionRetrieveUpdateDestroyView.as_view(), 
        name='question-detail',
    ),
    


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # *** ) Question In Banks *** # 
    path(
        'question-bank/questions/search/<str:searchstring>/', 
        views.QuestionInBankSearchList.as_view(),
        name="question-in-bank-search-list",
    ),
    # (Pk Search)
    path(
        'question-bank/<int:bank_id>/questions/search/<str:searchstring>/', 
        views.BanksQuestionInBankSearchList.as_view(),
        name="question-in-bank-search-list",
    ),
    
    # path(
    #     '---------------------------------------------------------------------------------------------------------------/', 
    #     views.Space.as_view(),
    # ),
    # Choice URLs
    # path(
    #     'question-bank/questions/choices/list/', 
    #     views.ChoiceListCreateView.as_view(), 
    #     name='choice-list',
    # ),
    # path(
    #     'question-bank/questions/choices/<int:pk>/', 
    #     views.ChoiceRetrieveUpdateDestroyView.as_view(), 
    #     name='choice-detail',
    # ),


    
    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # *** ) Student Questions Banks Result *** #
    # (List)
    path(
        "student-questionbank/result/list-app/",
        views.StudentQuestionBankResultListApp.as_view(),
        name="student-question-bank-result-list",
    ),
    # (PK)
    path(
        "student-questionbank/result/<int:pk>/",
        views.StudentQuestionBankResultPK.as_view(),
        name="student-question-bank-result-pk",
    ),
    # (Pk Results)
    path(
        'question-bank/<int:bank_id>/results/', 
        views.StudentQuestionBankResultBankList.as_view(), 
        name="student-question-bank-result-bank-list",
    ),
    # (Pk User)
    path(
        'question-bank/results/<int:user_id>/', 
        views.StudentQuestionBankResultUserList.as_view(), 
        name="student-question-bank-result-bank-list",
    ),

    


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),


    

    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # ================================================================
    # *** 1) ContactUs *** #
    # (List)
    path(
        "contactus-user/list/",
        views.ContactUsListAPIView.as_view(),
        name="contactus-list",
    ),
    # (PK)
    path(
        "contactus-user/<int:pk>/",
        views.ContactUsPKAPIView.as_view(),
        name="contactus-details-pk",
    ),
    # (Search)
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
    # (List)
    path(
        "review-user/list/",
        views.ReviewUserListAPIView.as_view(),
        name="review-user-list",
    ),
    # (List App)
    path(
        "review-user/list-app/",
        views.ReviewUserListApp.as_view(),
        name="review-user-list",
    ),
    # (List Result)
    path(
        "review-user/result/", #?result=5
        views.ReviewUserResultList.as_view(),
        name="review-user-list",
    ),
    # (PK)
    path(
        "review-user/<int:pk>/",
        views.ReviewUserPKAPIView.as_view(),
        name="review-user-details-pk",
    ),
    # (Search)
    path(
        'review-user/search/<str:searchstring>/', 
        views.ReviewUserSearchList.as_view(),
        name="review-user-search-list",
    ),




    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # =================================================================
    # *** ) Stats *** #
    # (App)
    path(
        'app-stats/',
        views.AppStatsView.as_view(), 
        name='app-stats',
    ),
    # (Admin)
    path(
        'admin-dashboard-stats/', # ?user_id=1/
        views.AdminDashboardStatsView.as_view(), 
        name='admin-dashboard-stats',
    ),
    # (Teacher)
    path(
        'teacher-dashboard-stats/', # ?user_id=1/
        views.TeacherDashboardStatsView.as_view(), 
        name='teacher-dashboard-stats',
    ),
    # (Student)
    path(
        'student-dashboard-stats/', # ?user_id=1/
        views.StudentDashboardStatsView.as_view(), 
        name='student-dashboard-stats',
    ),


 


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
