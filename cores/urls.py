from django.urls import path, include


#
from rest_framework_simplejwt.views import TokenRefreshView


#
from cores import views


urlpatterns = [
    # =================================================================
    # *** Cores Projects *** #
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
