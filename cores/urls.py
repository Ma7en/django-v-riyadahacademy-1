from django.urls import path, include


#
from rest_framework_simplejwt.views import TokenRefreshView


#
from cores import views


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
        'search-courses/<str:searchstring>', 
        views.CourseList.as_view(),
        name="course-search",
    ),
    
    # =================================================================
    # ***  *** #
    
    # =================================================================
    # *** Student Enroll Course *** #
    path(
        'student-enroll-course/', 
        views.StudentEnrollCourseList.as_view(),
        name="student-enroll-course",
    ),

    path(
        'student-enroll-course/list/', 
        views.StudentEnrollCourseList.as_view(),
        name="student-enroll-course-list",
    ),
    
    path(
        'fetch-enroll-status/<int:student_id>/<int:course_id>', 
        views.fetch_enroll_status,
        name="fetch-enroll-status-student_id-course_id",
    ),

    path(
        'fetch-enrolled-courses/<int:student_id>', 
        views.EnrolledStuentList.as_view(),
        name="fetch-enrolled-courses-student_id",
    ),

    path(
        'fetch-enrolled-students/<int:course_id>', 
        views.EnrolledStuentList.as_view(),
        name="fetch-enrolled-students-course_id",
    ),

    path(
        'fetch-recomemded-coourses/<int:student_id>', 
        views.EnrolledStuentList.as_view(),
        name="fetch-recomemded-coourses-student_id",
    ),

    path(
        'fetch-all-enrolled-students/<int:teacher_id>', 
        views.EnrolledStuentList.as_view(),
        name="fetch-all-enrolled-students-teacher_id",
    ),

    path(
        'student-enroll-course/<int:pk>', 
        views.StudentEnrollCoursePK.as_view(),
        name="student-enroll-course-pk",
    ),


    # =================================================================
    # *** Course Rating *** #
    path(
        'course-rating/', 
        views.CourseRatingList.as_view(),
        name="course-rating",
    ),

    path(
        'course-rating/list/', 
        views.CourseRatingList.as_view(),
        name="course-rating-list",
    ),

    path(
        'popular-courses/', 
        views.CourseRatingList.as_view(),
        name="popular-courses",
    ),

    path(
        'fetch-rating-status/<int:student_id>/<int:course_id>', 
        views.fetch_rating_status,
        name="fetch-rating-status-student_id-course_id",
    ),

    path(
        'course-rating/<int:pk>/', 
        views.CourseRatingPK.as_view(),
        name="course-rating-pk",
    ),


    # =================================================================
    # *** Student Favorite Course *** #
    path(
        'student-add-favorte-course/', 
        views.StudentFavoriteCourseList.as_view(),
        name="student-add-favorte-course-list",
    ),

    path(
        'student-add-favorte-course/list/', 
        views.StudentFavoriteCourseList.as_view(),
        name="student-add-favorte-course-list",
    ),

    path(
        'student-remove-favorite-course/<int:course_id>/<int:student_id>', 
        views.remove_favorite_course,
        name="student-remove-favorite-course-course_id-student_id",
    ),

    path(
        'fetch-favorite-coourses/<int:student_id>', 
        views.StudentFavoriteCourseList.as_view(),
        name="fetch-favorite-coourses-student_id",
    ),

    path(
        'student-favorite-coourses/<int:pk>', 
        views.StudentFavoriteCoursePK.as_view(),
        name="student-favorite-coourses-pk",
    ),

    # =================================================================
    # *** Teacher Student Chat *** #
    path(
        'send-message/<int:teacher_id>/<int:student_id>', 
        views.ChatBot, 
        name="Chat-Bot",
    ),

    path(
        'get-message/<int:teacher_id>/<int:student_id>', 
        views.MessageList.as_view(), 
        name="Message-List",
    ),

    path(
        'send-group-message/<int:teacher_id>', 
        views.GroupChatBot, 
        name="Group-Chat-Bot",
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
        name="review-list",
    ),
    path(
        "review-user/<int:pk>/",
        views.ReviewUserPKAPIView.as_view(),
        name="review-details-pk",
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
