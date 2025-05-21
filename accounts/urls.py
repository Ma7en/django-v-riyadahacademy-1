from django.urls import path, include


#
from rest_framework_simplejwt.views import TokenRefreshView


#
from accounts import views


urlpatterns = [
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
    # (Profile)
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
    # (Profile)
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
    # (Profile)
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
    # (Profile)
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
    
    # =================================================================
    # *** 5) Public *** #
    # (Students)
    path(
        "public/users-list/",
        views.UsersListView.as_view(),
        name="public-users-list-api",
    ),
    # (Student ID)
    path(
        "public/user/<int:pk>/",
        views.UserPKAPIView.as_view(),
        name="public-user-pk-api",
    ),
    # (Login)
    path(
        "public/login/",
        views.PublicLoginView.as_view(),
        name="public-login-api",
    ),
    # (ID)
    path(
        "public/<int:pk>/",
        views.PublicIDView.as_view(),
        name="public-user-id-api",
    ),

    # =================================================================
    # (Token Refreshing)
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    # =================================================================
]
