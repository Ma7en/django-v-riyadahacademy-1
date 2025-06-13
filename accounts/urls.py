# 
from django.urls import path, include


#
from rest_framework_simplejwt.views import TokenRefreshView


#
from . import views




urlpatterns = [
    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # =================================================================
    # *** User auths API Endpoints *** #
    # ================================================================
    # *** 1) Admin *** #
    # (Registration)
    path(
        "admin/register/",
        views.AdminRegisterView.as_view(),
        name="admin-register-api",
    ),
    # (Registration Verify)
    path(
        "admin/register-verify/",
        views.AdminRegisterVerifyView.as_view(),
        name="admin-register-verify-api",
    ),
    # (Admins)
    path(
        "admin/admins-list/",
        views.AdminsListView.as_view(),
        name="admin-admins-list-api",
    ),
    # (Admin ID)
    path(
        "admin/pk/<int:pk>/",
        views.AdminPKAPIView.as_view(),
        name="admin-pk-api",
    ),
    # (ID)
    path(
        "admin/<int:pk>/",
        views.AdminIDView.as_view(),
        name="admin-user-id",
    ),
    # (Profiles)
    path(
        "admin/profile-list/",
        views.AdminProfileList.as_view(),
        name="admin-profile-id",
    ),
    # (Profile ID)
    path(
        "admin/profile/<int:pk>/",
        views.AdminProfileView.as_view(),
        name="admin-profile-id",
    ),
    # (Resend OTP)
    path(
        "admin/resend-otp/",
        views.AdminResendOTPView.as_view(),
        name="admin-resend-otp-api",
    ),
    # (Verify Account)
    path(
        "admin/verify-account/",
        views.AdminVerifyAccountView.as_view(),
        name="verify-account-api",
    ),
    # (Login)
    path(
        "admin/login/",
        views.AdminLoginView.as_view(),
        name="admin-login-api",
    ),
    # (Refresh)
    path(
        "admin/refresh/",
        views.AdminRefreshView.as_view(),
        name="admin-user-refresh",
    ),
    # (Change Password)
    path(
        "admin/change-password/",
        views.AdminChangePasswordView.as_view(),
        name="admin-change-password-api",
    ),
    # (Logout)
    path(
        "admin/logout/",
        views.AdminLogoutView.as_view(),
        name="admin-logout-api",
    ),
    # (Reset Password)
    path(
        "admin/reset-password/",
        views.AdminPasswordResetView.as_view(),
        name="admin-reset-password-api",
    ),
    # (Confirm Reset Password)
    path(
        "admin/confirm-reset-password/",
        views.AdminConfirmResetPasswordView.as_view(),
        name="admin-confirm-reset-password",
    ),

    path(
        'admins/search/<str:searchstring>/', 
        views.AdminsSearchList.as_view(),
        name="admins-search-list",
    ),


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # ================================================================
    # *** 2) Teacher *** #
    # (Registration)
    path(
        "teacher/register/",
        views.TeacherRegisterView.as_view(),
        name="teacher-register-api",
    ),
    # (Registration Verify)
    path(
        "teacher/register-verify/",
        views.TeacherRegisterVerifyView.as_view(),
        name="teacher-register-verify-api",
    ),
    # (Teachers)
    path(
        "teacher/teachers-list/",
        views.TeachersListView.as_view(),
        name="teacher-teachers-list-api",
    ),
    # (Teacher ID)
    path(
        "teacher/pk/<int:pk>/",
        views.TeacherPKAPIView.as_view(),
        name="teacher-pk-api",
    ),
    # (ID)
    path(
        "teacher/<int:pk>/",
        views.TeacherIDView.as_view(),
        name="teacher-user-id",
    ),
    # (Profiles)
    path(
        "teacher/profile-list/",
        views.TeacherProfileList.as_view(),
        name="teacher-profile-id",
    ),
    # (Profile ID)
    path(
        "teacher/profile/<int:pk>/",
        views.TeacherProfileView.as_view(),
        name="teacher-profile-id",
    ),
    # (Resend OTP)
    path(
        "teacher/resend-otp/",
        views.TeacherResendOTPView.as_view(),
        name="teacher-resend-otp-api",
    ),
    # (Verify Account)
    path(
        "teacher/verify-account/",
        views.TeacherVerifyAccountView.as_view(),
        name="verify-account-api",
    ),
    # (Login)
    path(
        "teacher/login/",
        views.TeacherLoginView.as_view(),
        name="teacher-login-api",
    ),
    # (Refresh)
    path(
        "teacher/refresh/",
        views.TeacherRefreshView.as_view(),
        name="teacher-user-refresh",
    ),
    # (Change Password)
    path(
        "teacher/change-password/",
        views.TeacherChangePasswordView.as_view(),
        name="teacher-change-password-api",
    ),
    # (Logout)
    path(
        "teacher/logout/",
        views.TeacherLogoutView.as_view(),
        name="teacher-logout-api",
    ),
    # (Reset Password)
    path(
        "teacher/reset-password/",
        views.TeacherPasswordResetView.as_view(),
        name="teacher-reset-password-api",
    ),
    # (Confirm Reset Password)
    path(
        "teacher/confirm-reset-password/",
        views.TeacherConfirmResetPasswordView.as_view(),
        name="teacher-confirm-reset-password",
    ),


    path(
        'teachers/search/<str:searchstring>/', 
        views.TeachersSearchList.as_view(),
        name="teachers-search-list",
    ),


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # ================================================================
    # *** 3) Staff *** #
    # (Registration)
    path(
        "staff/register/",
        views.StaffRegisterView.as_view(),
        name="staff-register-api",
    ),
    # (Registration Verify)
    path(
        "staff/register-verify/",
        views.StaffRegisterVerifyView.as_view(),
        name="staff-register-verify-api",
    ),
    # (Staffs)
    path(
        "staff/staffs-list/",
        views.StaffsListView.as_view(),
        name="staff-staffs-list-api",
    ),
    # (Staff ID)
    path(
        "staff/pk/<int:pk>/",
        views.StaffPKAPIView.as_view(),
        name="staff-pk-api",
    ),
    # (ID)
    path(
        "staff/<int:pk>/",
        views.StaffIDView.as_view(),
        name="staff-user-id",
    ),
    # (Profiles)
    path(
        "staff/profile-list/",
        views.StaffProfileList.as_view(),
        name="staff-profile-id",
    ),
    # (Profile ID)
    path(
        "staff/profile/<int:pk>/",
        views.StaffProfileView.as_view(),
        name="staff-profile-id",
    ),
    # (Resend OTP)
    path(
        "staff/resend-otp/",
        views.StaffResendOTPView.as_view(),
        name="staff-resend-otp-api",
    ),
    # (Verify Account)
    path(
        "staff/verify-account/",
        views.StaffVerifyAccountView.as_view(),
        name="verify-account-api",
    ),
    # (Login)
    path(
        "staff/login/",
        views.StaffLoginView.as_view(),
        name="staff-login-api",
    ),
    # (Refresh)
    path(
        "staff/refresh/",
        views.StaffRefreshView.as_view(),
        name="staff-user-refresh",
    ),
    # (Change Password)
    path(
        "staff/change-password/",
        views.StaffChangePasswordView.as_view(),
        name="staff-change-password-api",
    ),
    # (Logout)
    path(
        "staff/logout/",
        views.StaffLogoutView.as_view(),
        name="staff-logout-api",
    ),
    # (Reset Password)
    path(
        "staff/reset-password/",
        views.StaffPasswordResetView.as_view(),
        name="staff-reset-password-api",
    ),
    # (Confirm Reset Password)
    path(
        "staff/confirm-reset-password/",
        views.StaffConfirmResetPasswordView.as_view(),
        name="staff-confirm-reset-password",
    ),

    path(
        'staffs/search/<str:searchstring>/', 
        views.StaffsSearchList.as_view(),
        name="staffs-search-list",
    ),


    
    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # ================================================================
    # *** 4) Student *** #
    # (Registration)
    path(
        "student/register/",
        views.StudentRegisterView.as_view(),
        name="student-register-api",
    ),
    # (Registration Verify)
    path(
        "student/register-verify/",
        views.StudentRegisterVerifyView.as_view(),
        name="student-register-verify-api",
    ),
    # (Students)
    path(
        "student/students-list/",
        views.StudentsListView.as_view(),
        name="student-students-list-api",
    ),
    # (Students Admin)
    path(
        "student/students-list-admin/",
        views.StudentsListAdmin.as_view(),
        name="student-students-list-admin-api",
    ),
    # (Student ID)
    path(
        "student/pk/<int:pk>/",
        views.StudentPKAPIView.as_view(),
        name="student-pk-api",
    ),
    # (ID)
    path(
        "student/<int:pk>/",
        views.StudentIDView.as_view(),
        name="student-user-id",
    ),
    # (Profiles)
    path(
        "student/profile-list/",
        views.StudentProfileList.as_view(),
        name="student-profile-id",
    ),
    # (Profile ID)
    path(
        "student/profile/<int:pk>/",
        views.StudentProfileView.as_view(),
        name="student-profile-id",
    ),
    # (Resend OTP)
    path(
        "student/resend-otp/",
        views.StudentResendOTPView.as_view(),
        name="student-resend-otp-api",
    ),
    # (Verify Account)
    path(
        "student/verify-account/",
        views.StudentVerifyAccountView.as_view(),
        name="verify-account-api",
    ),
    # (Login)
    path(
        "student/login/",
        views.StudentLoginView.as_view(),
        name="student-login-api",
    ),
    # (Refresh)
    path(
        "student/refresh/",
        views.StudentRefreshView.as_view(),
        name="student-user-refresh",
    ),
    # (Change Password)
    path(
        "student/change-password/",
        views.StudentChangePasswordView.as_view(),
        name="student-change-password-api",
    ),
    # (Logout)
    path(
        "student/logout/",
        views.StudentLogoutView.as_view(),
        name="student-logout-api",
    ),
    # (Reset Password)
    path(
        "student/reset-password/",
        views.StudentPasswordResetView.as_view(),
        name="student-reset-password-api",
    ),
    # (Confirm Reset Password)
    path(
        "student/confirm-reset-password/",
        views.StudentConfirmResetPasswordView.as_view(),
        name="student-confirm-reset-password",
    ),
    
    path(
        'students/search/<str:searchstring>/', 
        views.StudentsSearchList.as_view(),
        name="students-search-list",
    ),



    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # =================================================================
    # *** 5) Public *** #
    # (Users)
    path(
        "public/users-list/",
        views.PublicUsersListView.as_view(),
        name="public-users-list-api",
    ),
    # (User ID)
    path(
        "public/user/<int:pk>/",
        views.PublicUserPKAPIView.as_view(),
        name="public-user-pk-api",
    ),
    # (ID)
    path(
        "public/<int:pk>/",
        views.PublicIDView.as_view(),
        name="public-user-id-api",
    ),
    # (Verify Account)
    path(
        "public/verify-account/",
        views.PublicVerifyAccountView.as_view(),
        name="verify-account-api",
    ),
    # (Resend OTP)
    path(
        "public/resend-otp/",
        views.PublicResendOTPView.as_view(),
        name="public-resend-otp-api",
    ),
    # (Login)
    path(
        "public/login/",
        views.PublicLoginView.as_view(),
        name="public-login-api",
    ),
    # (Refresh)
    path(
        "public/refresh/",
        views.PublicRefreshView.as_view(),
        name="public-user-refresh",
    ),
    # (Change Password)
    path(
        "public/change-password/",
        views.PublicChangePasswordView.as_view(),
        name="public-change-password-api",
    ),
    # (Logout)
    path(
        "public/logout/",
        views.PublicLogoutView.as_view(),
        name="public-logout-api",
    ),
    # (Reset Password)
    path(
        "public/reset-password/",
        views.PublicPasswordResetView.as_view(),
        name="public-reset-password-api",
    ),
    # (Confirm Reset Password)
    path(
        "public/confirm-reset-password/",
        views.PublicConfirmResetPasswordView.as_view(),
        name="public-confirm-reset-password",
    ),
    path(
        'public/user/search/<str:searchstring>/', 
        views.PublicUserSearchList.as_view(),
        name="public-user-search-list",
    ),



    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # =================================================================
    # (Token Refreshing)
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),


    path(
        '---------------------------------------------------------------------------------------------------------------/', 
        views.Space.as_view(),
    ),
    # =================================================================
]
