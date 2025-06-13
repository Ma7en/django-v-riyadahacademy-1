#
import jwt



#
from django.shortcuts import render
from smtplib import SMTPRecipientsRefused
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q




# 
SECRET_KEY = settings.SECRET_KEY



#
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response 
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)



#
from . import models, serializers, utils
# from . import validations





# ******************************************************************************
# ==============================================================================
# *** 0) Pagination *** #
class StandardResultSetPagination(PageNumberPagination):
    page_size=9
    page_size_query_param='page_size'
    max_page_size = 100


class Space(generics.ListCreateAPIView):
    pass





# ******************************************************************************
# ==============================================================================
# *** 1) Admin *** #
# *** Admin (Register) -> [POST] *** #
class AdminRegisterView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.AdminRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.AdminRegisterSerializer(data=request.data)

        if serializer.is_valid():
            # Step 1: Save the user data using the serializer's create method
            admin = serializer.save()
            admin_data = serializers.UserSerializer(admin).data

            # Step 2: Send OTP to the admin's email using the utility function
            try:
                # Call the email-sending function
                utils.send_otp_for_user(admin.email, "admin")
            except SMTPRecipientsRefused as e:
                raise ValidationError(
                    {
                        "Error": f"Error sending OTP to {admin.email}: {e}",
                    }
                )

            # Step 3: Return success response
            message = (
                "Admin registered successfully, and We have sent an OTP to your Email!"
            )
            return utils.FunReturn(
                0,
                message,
                status.HTTP_201_CREATED,
                admin_data,
            )

        # Step 4:
        message = serializer.errors
        return utils.FunReturn(
            1,
            message,
            status.HTTP_400_BAD_REQUEST,
        )


# *** Admin (Register Verify) -> [POST] *** #
class AdminRegisterVerifyView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.AdminRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.AdminRegisterSerializer(data=request.data)

        if serializer.is_valid():
            # Step 1: Save the user data using the serializer's create method
            admin = serializer.save()
            admin.is_verified = True
            admin.save()
            admin_data = serializers.UserSerializer(admin).data

            # Step 2: Return success response
            message = (
                "Admin Registered Successfully."
            )
            return utils.FunReturn(
                0,
                message,
                status.HTTP_201_CREATED,
                admin_data,
            )

        # Step 3:
        message = serializer.errors
        return utils.FunReturn(
            1,
            message,
            status.HTTP_400_BAD_REQUEST,
        )


# *** Admin (Admins) -> [GET, POST] *** #
class AdminsListView(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_admin=True)
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]


# *** Admin (Admin ID) -> [GET, POST, PUT, DELETE] *** #
class AdminPKAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_admin=True)
    # permission_classes = [IsAuthenticated]


# *** Admin (ID) -> [GET] *** #
class AdminIDView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def get(self, request, pk):
        try:
            admin = models.User.objects.get(pk=pk)
        except models.User.DoesNotExist:
            message = "Admin not found."
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)

        admin_data = self.get_serializer(admin).data
        if admin_data["is_admin"] == False:
            message = "Admin with this id is not Found."
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)

        try:
            admin_profile = models.AdminProfile.objects.get(user=admin)
            admin_profile_data = serializers.AdminProfileSerializer(admin_profile).data
        except models.AdminProfile.DoesNotExist:
            admin_profile_data = None

        message = "Admin retrieved Successfully."
        return Response({
            "success": "True",
            "code": 0,
            "message": message,
            "status_code": status.HTTP_200_OK,
            "data": admin_data,
            "profile": admin_profile_data,
        }, status.HTTP_200_OK)


# *** Admin (Profiles) -> [GET, POST] *** #
class AdminProfileList(generics.ListCreateAPIView):
    serializer_class = serializers.AdminProfileSerializer
    queryset = models.AdminProfile.objects.all()
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]


# *** Admin (Profile ID) -> [GET, PUT, PATCH, DELETE] *** #
class AdminProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AdminProfileSerializer
    queryset = models.AdminProfile.objects.all()
    # permission_classes = [IsAuthenticated]


# *** Admin (Profile ID) -> [GET, PUT, PATCH, DELETE] *** #
# class AdminProfileView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = serializers.AdminProfileSerializer
#     queryset = models.AdminProfile.objects.all()
#     # permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return models.AdminProfile.objects.all()

#     def get_object(self):
#         try:
#             admin_pk = self.kwargs["pk"]  # 1
#             admin_profile = models.AdminProfile.objects.get(user=admin_pk)
#             return admin_profile
#         except models.AdminProfile.DoesNotExist:
#             status_code = status.HTTP_404_NOT_FOUND
#             raise NotFound(
#                 {
#                     "success": "False",
#                     "code": 1,
#                     "message": "Admin Profile not found.",
#                     "status_code": status_code,
#                     "data": "",
#                 }
#             )

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         admin_data = serializer.data

#         if admin_data["user"]["is_admin"] == False:
#             message = "Admin Profile whit this id is not Found."
#             return utils.FunReturn(
#                 1,
#                 message,
#                 status.HTTP_404_NOT_FOUND,
#             )

#         message = "Admin Profile retrieved Successfully."
#         return utils.FunReturn(
#             0,
#             message,
#             status.HTTP_200_OK,
#             admin_data,
#         )

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop("partial", False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         admin_data = serializer.data
#         message = "Admin Profile updated Successfully."
#         return utils.FunReturn(
#             0,
#             message,
#             status.HTTP_200_OK,
#             admin_data,
#         )


# *** Admin (Resend OTP) -> [POST] *** #
class AdminResendOTPView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.AdminResendOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        try:
            user = models.User.objects.get(email=email)
            if user.is_verified:
                message = "Your account has already been verified. Please go to the login page."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN)

            utils.send_otp_for_user(user.email, "admin")
        except models.User.DoesNotExist:
            message = "No user found with this email."
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)

        message = "OTP has been resent to your email."
        return utils.FunReturn(0, message, status.HTTP_200_OK)


# *** Admin (Verify Account) -> [POST] *** #
class AdminVerifyAccountView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.AdminVerifyAccountSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        otp_code = serializer.validated_data["otp_code"]
        try:
            otp = models.OneTimeOTP.objects.get(otp=otp_code)
        except models.OneTimeOTP.DoesNotExist:
            message = "Invalid OTP Code"
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        if otp.is_expired():
            message = "OTP has expired"
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        if otp.user:
            user = otp.user
        else:
            message = "No associated user for this OTP code"
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        if user.is_verified:
            message = "Email already verified"
            admin_data = serializers.UserSerializer(user).data
            return utils.FunReturn(0, message, status.HTTP_200_OK, admin_data)

        user.is_verified = True
        user.save()
        utils.send_verification_email(user, otp_code)
        otp.delete()
        admin_data = serializers.UserSerializer(user).data
        message = "Email verified Successfully"
        return utils.FunReturn(0, message, status.HTTP_200_OK, admin_data)


# *** Admin (Login) -> [POST] *** # 
class AdminLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.AdminLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            admin = serializer.validated_data

            if not admin.is_verified:
                message = "Your account is not verified. Please verify your account to proceed."
                return utils.FunReturn(
                    1, 
                    message, 
                    status.HTTP_403_FORBIDDEN, 
                    serializer.validated_data,
                )

            refresh = RefreshToken.for_user(admin)
            refresh["admin_id"] = admin.id
            access_token = refresh.access_token

            try:
                admin_profile = models.AdminProfile.objects.get(user=admin)
                admin_profile_data = serializers.AdminProfileSerializer(admin_profile).data
            except models.AdminProfile.DoesNotExist:
                admin_profile_data = None

            admin_data = serializers.UserSerializer(admin).data
            response = {
                "success": "True",
                "code": 0,
                "message": "Admin Login Successfully.",
                "status_code": status.HTTP_200_OK,
                "data": admin_data,
                "profile": admin_profile_data,
                "access_token": str(access_token),
                "refresh_token": str(refresh),
            }
            return Response(response, status=status.HTTP_200_OK)
        return utils.FunReturn(
            1, 
            serializer.errors, 
            status.HTTP_400_BAD_REQUEST,
            )


# *** Admin (Refresh) -> [POST] *** # 
class AdminRefreshView(generics.GenericAPIView):
    serializer_class = serializers.AdminRefreshSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data["refresh_token"]
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                message = {"refresh_token": "Invalid token payload."}
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

            admin = models.User.objects.get(id=user_id)
            admin_data = serializers.UserSerializer(admin).data
            message = "Admin retrieved successfully."
            return utils.FunReturn(0, message, status.HTTP_200_OK, admin_data)
        except models.User.DoesNotExist:
            message = {"message": "Admin not found."}
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            message = {"message": "Refresh token has expired."}
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            message = {"message": "Invalid refresh token."}
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            message = {"message": str(e)}
            return utils.FunReturn(1, message, status.HTTP_500_INTERNAL_SERVER_ERROR)


# *** Admin (Change Password) -> [POST] *** # 
class AdminChangePasswordView(generics.GenericAPIView):
    serializer_class = serializers.AdminChangePasswordSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data["refresh_token"]
        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]
        confirm_password = serializer.validated_data["confirm_password"]

        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
            admin_id = payload.get("admin_id")
            admin = models.User.objects.get(id=admin_id)

            if not check_password(old_password, admin.password):
                message = "Old password is incorrect."
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_password:
                message = "New passwords do not match."
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

            admin.set_password(new_password)
            admin.save()
            utils.send_change_password_confirm(admin)
            admin_data = serializers.UserSerializer(admin).data
            message = "Password changed successfully."
            return utils.FunReturn(0, message, status.HTTP_200_OK, admin_data)
        except jwt.ExpiredSignatureError:
            message = "Token has expired"
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            message = "Invalid token"
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except models.User.DoesNotExist:
            message = "Admin not found"
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)
        

# *** Admin (Logout) -> [POST] *** # 
class AdminLogoutView(generics.GenericAPIView):
    serializer_class = serializers.AdminLogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data["refresh_token"]
        try:
            token = RefreshToken(refresh_token)
            admin_id_in_token = token.payload.get("user_id")
            if not admin_id_in_token:
                message = "Invalid token: user id missing."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN)

            admin = models.User.objects.filter(id=admin_id_in_token).first()
            if not admin:
                message = "Invalid token: admin not found."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN)

            # token.blacklist()  # بدلاً من token.set_exp()
            token.set_exp()
            message = "Logout successful."
            return utils.FunReturn(0, message, status.HTTP_200_OK)
        except Exception as e:
            message = str(e)
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)


# *** Admin (Reset Password) -> [POST] *** # 
class AdminPasswordResetView(generics.GenericAPIView):
    serializer_class = serializers.AdminPasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        try:
            admin = models.User.objects.get(email=email)
            admin_data = serializers.UserSerializer(admin).data
            if not admin.is_verified:
                message = "Your account is not verified. Please verify your account to proceed."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN, admin_data)
        except models.User.DoesNotExist:
            message = "Admin with this email does not exist."
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        try:
            utils.send_otp_for_password_reset(email, user_type="admin")
            message = "OTP has been sent to your email."
            return utils.FunReturn(0, message, status.HTTP_200_OK, admin_data)
        except ValueError as e:
            message = str(e)
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)


# *** Admin (Confirm Reset Password) -> [POST] *** # 
class AdminConfirmResetPasswordView(generics.GenericAPIView):
    serializer_class = serializers.AdminConfirmResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        otp = serializer.validated_data["otp"]
        password = serializer.validated_data["password"]

        try:
            otp_instance = models.OneTimeOTP.objects.get(otp=otp, user__isnull=False)
            if otp_instance.is_expired():
                message = "OTP has expired."
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)
        except models.OneTimeOTP.DoesNotExist:
            message = "Invalid OTP."
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        admin = otp_instance.user
        admin.set_password(password)
        admin.save()
        utils.send_reset_password_confirm(admin)
        models.OneTimeOTP.objects.filter(user=admin).delete()
        admin_data = serializers.UserSerializer(admin).data
        message = "Confirm Reset Password Successfully."
        return utils.FunReturn(0, message, status.HTTP_200_OK, admin_data)
    

# *** Admin (Search) -> [GET] *** #
# class AdminsSearchList(generics.ListCreateAPIView):
#     queryset = models.User.objects.filter(is_admin=True)
#     serializer_class = serializers.UserSerializer
#     pagination_class = StandardResultSetPagination
#     # permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         qs = super().get_queryset()

#         if 'searchstring' in self.kwargs:
#             search = self.kwargs['searchstring'] 
#             qs = qs.filter(
#                 Q(full_name__icontains=search)
#                 |Q(username__icontains=search)
#                 |Q(email__icontains=search)
#                 )
#         return qs

# *** Admin (Search) -> [GET] *** #
class AdminsSearchList(generics.ListCreateAPIView):
    queryset = models.AdminProfile.objects.filter()
    serializer_class = serializers.AdminProfileSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring'] 
            qs = qs.filter(
                Q(user__full_name__icontains=search)
                |Q(user__username__icontains=search)
                |Q(user__email__icontains=search)
                )
        return qs






# ******************************************************************************
# ==============================================================================
# *** 2) Teacher *** #
# *** Teacher (Register) -> [POST] *** #
class TeacherRegisterView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.TeacherRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.TeacherRegisterSerializer(data=request.data)

        if serializer.is_valid():
            # Step 1: Save the user data using the serializer's create method
            teacher = serializer.save()
            teacher_data = serializers.UserSerializer(teacher).data

            # Step 2: Send OTP to the teacher's email using the utility function
            try:
                # Call the email-sending function
                utils.send_otp_for_user(teacher.email, "teacher")
            except SMTPRecipientsRefused as e:
                raise ValidationError(
                    {
                        "Error": f"Error sending OTP to {teacher.email}: {e}",
                    }
                )

            # Step 3: Return success response
            message = "Teacher registered successfully, and We have sent an OTP to your Email!"
            return utils.FunReturn(
                0,
                message,
                status.HTTP_201_CREATED,
                teacher_data,
            )

        message = serializer.errors
        return utils.FunReturn(
            1,
            message,
            status.HTTP_400_BAD_REQUEST,
        )


# *** Teacher (Register Verify) -> [POST] *** #
class TeacherRegisterVerifyView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.TeacherRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.TeacherRegisterSerializer(data=request.data)

        if serializer.is_valid():
            # Step 1: Save the user data using the serializer's create method
            teacher = serializer.save()
            teacher.is_verified = True
            teacher.save()
            teacher_data = serializers.UserSerializer(teacher).data


            # Step 2: Return success response
            message = "Teacher Registered Successfully."
            return utils.FunReturn(
                0,
                message,
                status.HTTP_201_CREATED,
                teacher_data,
            )

        # Step 3:
        message = serializer.errors
        return utils.FunReturn(
            1,
            message,
            status.HTTP_400_BAD_REQUEST,
        )


# *** Teacher (Teachers) -> [GET, POST] *** #
class TeachersListView(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_teacher=True)
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]


# *** Teacher (Teacher ID) -> [GET, POST, PUT, DELETE] *** #
class TeacherPKAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_teacher=True)
    # permission_classes = [IsAuthenticated]


# *** Teacher (ID) -> [GET] *** #
class TeacherIDView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def get(self, request, pk):
        try:
            teacher = models.User.objects.get(pk=pk)
        except models.User.DoesNotExist:
            message = "Teacher not found."
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)

        teacher_data = self.get_serializer(teacher).data
        if teacher_data["is_teacher"] == False:
            message = "Teacher with this Id is not Found."
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)

        try:
            teacher_profile = models.TeacherProfile.objects.get(user=teacher)
            teacher_profile_data = serializers.TeacherProfileSerializer(teacher_profile).data
        except models.TeacherProfile.DoesNotExist:
            teacher_profile_data = None

        message = "Teacher retrieved Successfully."
        return Response({
            "success": "True",
            "code": 0,
            "message": message,
            "status_code": status.HTTP_200_OK,
            "data": teacher_data,
            "profile": teacher_profile_data,
        }, status.HTTP_200_OK)


# *** Teacher (Profiles) -> [GET, POST] *** #
class TeacherProfileList(generics.ListCreateAPIView):
    serializer_class = serializers.TeacherProfileSerializer
    queryset = models.TeacherProfile.objects.all()
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]


# *** Teacher (Profile ID) -> [GET, PUT, PATCH, DELETE] *** #
class TeacherProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TeacherProfileSerializer
    queryset = models.TeacherProfile.objects.all()
    # permission_classes = [IsAuthenticated]


# *** Teacher (Profile ID) -> [GET, PUT, PATCH, DELETE] *** #
# class TeacherProfileView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = serializers.TeacherProfileSerializer
#     # permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return models.TeacherProfile.objects.all()

#     def get_object(self):
#         try:
#             teacher_pk = self.kwargs["pk"]  # 1
#             teacher_profile = models.TeacherProfile.objects.get(user=teacher_pk)
#             return teacher_profile
#         except models.TeacherProfile.DoesNotExist:
#             status_code = status.HTTP_404_NOT_FOUND
#             raise NotFound(
#                 {
#                     "success": "False",
#                     "code": 1,
#                     "message": "Teacher Profile not found",
#                     "status_code": status_code,
#                     "data": "",
#                 }
#             )

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         teacher_data = serializer.data

#         if teacher_data["user"]["is_teacher"] == False:
#             message = "Teacher Profile whit this id is not Found"
#             return utils.FunReturn(
#                 1,
#                 message,
#                 status.HTTP_404_NOT_FOUND,
#             )

#         message = "Teacher Profile retrieved successfully"
#         return utils.FunReturn(
#             0,
#             message,
#             status.HTTP_200_OK,
#             teacher_data,
#         )

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop("partial", False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         teacher_data = serializer.data
#         message = "Teacher Profile updated Successfully."
#         return utils.FunReturn(
#             0,
#             message,
#             status.HTTP_200_OK,
#             teacher_data,
#         )


# *** Teacher (Resend OTP) -> [POST] *** #
class TeacherResendOTPView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.TeacherResendOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        try:
            user = models.User.objects.get(email=email)
            if user.is_verified:
                message = "Your account has already been verified. Please go to the login page."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN)

            utils.send_otp_for_user(user.email, "teacher")
        except models.User.DoesNotExist:
            message = "No user found with this email."
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)

        message = "OTP has been resent to your email."
        return utils.FunReturn(0, message, status.HTTP_200_OK)


# *** Teacher (Verify Account) -> [POST] *** # 
class TeacherVerifyAccountView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.TeacherVerifyAccountSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        otp_code = serializer.validated_data["otp_code"]
        try:
            otp = models.OneTimeOTP.objects.get(otp=otp_code)
        except models.OneTimeOTP.DoesNotExist:
            message = "Invalid OTP Code"
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        if otp.is_expired():
            message = "OTP has expired"
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        if otp.user:
            user = otp.user
        else:
            message = "No associated user for this OTP code"
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        if user.is_verified:
            message = "Email already verified"
            teacher_data = serializers.UserSerializer(user).data
            return utils.FunReturn(0, message, status.HTTP_200_OK, teacher_data)

        user.is_verified = True
        user.save()
        utils.send_verification_email(user, otp_code)
        otp.delete()
        teacher_data = serializers.UserSerializer(user).data
        message = "Email verified Successfully."
        return utils.FunReturn(0, message, status.HTTP_200_OK, teacher_data)


# *** Teacher (Login) -> [POST] *** #
class TeacherLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.TeacherLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            teacher = serializer.validated_data
        
            if not teacher.is_verified:
                message = "Your account is not verified. Please verify your account to proceed."
                return utils.FunReturn(
                    1, 
                    message, 
                    status.HTTP_403_FORBIDDEN, 
                    serializer.validated_data,
                )

            refresh = RefreshToken.for_user(teacher)
            refresh["teacher_id"] = teacher.id
            access_token = refresh.access_token

            try:
                teacher_profile = models.TeacherProfile.objects.get(user=teacher)
                teacher_profile_data = serializers.TeacherProfileSerializer(teacher_profile).data
            except models.TeacherProfile.DoesNotExist:
                teacher_profile_data = None

            teacher_data = serializers.UserSerializer(teacher).data
            response = {
                "success": "True",
                "code": 0,
                "message": "Teacher Login Successfully.",
                "status_code": status.HTTP_200_OK,
                "data": teacher_data,
                "profile": teacher_profile_data,
                "access_token": str(access_token),
                "refresh_token": str(refresh),
            }
            return Response(response, status=status.HTTP_200_OK)
        return utils.FunReturn(
            1, 
            serializer.errors, 
            status.HTTP_400_BAD_REQUEST,
            )


# *** Teacher (Refresh) -> [POST] *** # 
class TeacherRefreshView(generics.GenericAPIView):
    serializer_class = serializers.TeacherRefreshSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data["refresh_token"]
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                message = {"refresh_token": "Invalid token payload."}
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

            teacher = models.User.objects.get(id=user_id)
            teacher_data = serializers.UserSerializer(teacher).data
            message = "Teacher retrieved Successfully."
            return utils.FunReturn(0, message, status.HTTP_200_OK, teacher_data)
        except models.User.DoesNotExist:
            message = {"message": "Teacher not found."}
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            message = {"message": "Refresh token has expired."}
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            message = {"message": "Invalid refresh token."}
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            message = {"message": str(e)}
            return utils.FunReturn(1, message, status.HTTP_500_INTERNAL_SERVER_ERROR)


# *** Teacher (Change Password) -> [POST] *** # 
class TeacherChangePasswordView(generics.GenericAPIView):
    serializer_class = serializers.TeacherChangePasswordSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data["refresh_token"]
        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]
        confirm_password = serializer.validated_data["confirm_password"]

        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["256"])
            teacher_id = payload.get("teacher_id")
            if not teacher_id:
                teacher_id = payload.get("user_id")

            teacher = models.User.objects.get(id=teacher_id)

            if not check_password(old_password, teacher.password):
                message = "Old password is incorrect."
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_password:
                message = "New passwords do not match."
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

            teacher.set_password(new_password)
            teacher.save()
            utils.send_change_password_confirm(teacher)
            teacher_data = serializers.UserSerializer(teacher).data
            message = "Password changed successfully."
            return utils.FunReturn(0, message, status.HTTP_200_OK, teacher_data)
        except jwt.ExpiredSignatureError:
            message = "Token has expired"
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            message = "Invalid token"
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except models.User.DoesNotExist:
            message = "Teacher not found"
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)


# *** Teacher (Logout) -> [POST] *** # 
class TeacherLogoutView(generics.GenericAPIView):
    serializer_class = serializers.TeacherLogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data["refresh_token"]
        try:
            token = RefreshToken(refresh_token)
            teacher_id_in_token = token.payload.get("user_id")
            if not teacher_id_in_token:
                message = "Invalid token: user_id missing."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN)

            teacher = models.User.objects.filter(id=teacher_id_in_token).first()
            if not teacher:
                message = "Invalid token: Teacher not found."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN)

            # token.blacklist()  # بدلاً من token.set_exp()
            token.set_exp()
            message = "Logout Successful."
            return utils.FunReturn(0, message, status.HTTP_200_OK)
        except Exception as e:
            message = str(e)
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)
        

# *** Teacher (Reset Password) -> [POST] *** # 
class TeacherPasswordResetView(generics.GenericAPIView):
    serializer_class = serializers.TeacherPasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        try:
            teacher = models.User.objects.get(email=email)
            teacher_data = serializers.UserSerializer(teacher).data
            if not teacher.is_verified:
                message = "Your account is not verified. Please verify your account to proceed."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN, teacher_data)
        except models.User.DoesNotExist:
            message = "Teacher with this email does not exist."
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        try:
            utils.send_otp_for_password_reset(email, user_type="teacher")
            message = "OTP has been sent to your email."
            return utils.FunReturn(0, message, status.HTTP_200_OK, teacher_data)
        except ValueError as e:
            message = str(e)
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)


# *** Teacher (Confirm Reset Password) -> [POST] *** # 
class TeacherConfirmResetPasswordView(generics.GenericAPIView):
    serializer_class = serializers.TeacherConfirmResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        otp = serializer.validated_data["otp"]
        password = serializer.validated_data["password"]

        try:
            otp_instance = models.OneTimeOTP.objects.get(otp=otp, user__isnull=False)
            if otp_instance.is_expired():
                message = "OTP has expired."
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)
        except models.OneTimeOTP.DoesNotExist:
            message = "Invalid OTP."
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        teacher = otp_instance.user
        teacher.set_password(password)
        teacher.save()
        utils.send_reset_password_confirm(teacher)
        models.OneTimeOTP.objects.filter(user=teacher).delete()
        teacher_data = serializers.UserSerializer(teacher).data
        message = "Confirm Reset Password Successfully."
        return utils.FunReturn(0, message, status.HTTP_200_OK, teacher_data)


# # *** Teacher (Search) -> [GET] *** #
# class TeachersSearchList(generics.ListCreateAPIView):
#     queryset = models.User.objects.filter(is_teacher=True)
#     serializer_class = serializers.UserSerializer
#     pagination_class = StandardResultSetPagination
#     # permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         qs = super().get_queryset()

#         if 'searchstring' in self.kwargs:
#             search = self.kwargs['searchstring'] 
#             qs = qs.filter(
#                 Q(full_name__icontains=search)
#                 |Q(username__icontains=search)
#                 |Q(email__icontains=search)
#                 )
#         return qs


# *** Teacher (Search) -> [GET] *** #
class TeachersSearchList(generics.ListCreateAPIView):
    queryset = models.TeacherProfile.objects.filter()
    serializer_class = serializers.TeacherProfileSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring'] 
            qs = qs.filter(
                Q(user__full_name__icontains=search)
                |Q(user__username__icontains=search)
                |Q(user__email__icontains=search)
                )
        return qs






# ******************************************************************************
# ==============================================================================
# *** 3) Staff *** #
# *** Staff (Register) -> [POST] *** #
class StaffRegisterView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.StaffRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.StaffRegisterSerializer(data=request.data)

        if serializer.is_valid():
            # Step 1: Save the user data using the serializer's create method
            staff = serializer.save()
            staff_data = serializers.UserSerializer(staff).data

            # Step 2: Send OTP to the staff's email using the utility function
            try:
                # Call the email-sending function
                utils.send_otp_for_user(staff.email, "staff")
            except SMTPRecipientsRefused as e:
                raise ValidationError(
                    {
                        "Error": f"Error sending OTP to {staff.email}: {e}",
                    }
                )

            # Step 3: Return success response
            message = (
                "Staff registered Successfully, and We have sent an OTP to your Email!"
            )
            return utils.FunReturn(
                0,
                message,
                status.HTTP_201_CREATED,
                staff_data,
            )

        # Step 4:
        message = serializer.errors
        return utils.FunReturn(
            1,
            message,
            status.HTTP_400_BAD_REQUEST,
        )


# *** Staff (Register Verify) -> [POST] *** #
class StaffRegisterVerifyView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.StaffRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.StaffRegisterSerializer(data=request.data)

        if serializer.is_valid():
            # Step 1: Save the user data using the serializer's create method
            staff = serializer.save()
            staff.is_verified = True
            staff.save()
            staff_data = serializers.UserSerializer(staff).data

            # Step 2: Return success response
            message = ("Staff Registered Successfully")
            return utils.FunReturn(
                0,
                message,
                status.HTTP_201_CREATED,
                staff_data,
            )

        # Step 3:
        message = serializer.errors
        return utils.FunReturn(
            1,
            message,
            status.HTTP_400_BAD_REQUEST,
        )


# *** Staff (Staffs) -> [GET, POST] *** #
class StaffsListView(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_staff=True)
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]


# *** Staff (Staff ID) -> [GET, POST, PUT, DELETE] *** #
class StaffPKAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_staff=True)
    # permission_classes = [IsAuthenticated]


# *** Staff (ID) -> [GET] *** #
class StaffIDView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def get(self, request, pk):
        try:
            staff = models.User.objects.get(pk=pk)
        except models.User.DoesNotExist:
            message = "Staff not found."
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)

        staff_data = self.get_serializer(staff).data
        if staff_data["is_staff"] == False:
            message = "Staff with this Id is not Found."
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)

        try:
            staff_profile = models.StaffProfile.objects.get(user=staff)
            staff_profile_data = serializers.StaffProfileSerializer(staff_profile).data
        except models.StaffProfile.DoesNotExist:
            staff_profile_data = None

        message = "Staff retrieved Successfully."
        return Response({
            "success": "True",
            "code": 0,
            "message": message,
            "status_code": status.HTTP_200_OK,
            "data": staff_data,
            "profile": staff_profile_data,
        }, status.HTTP_200_OK)


# *** Staff (Profiles) -> [GET, PUT] *** #
class StaffProfileList(generics.ListCreateAPIView):
    serializer_class = serializers.StaffProfileSerializer
    queryset = models.StaffProfile.objects.all()
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]


# *** Staff (Profile ID) -> [GET, PUT, PATCH, DELETE] *** #
class StaffProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.StaffProfileSerializer
    queryset = models.StaffProfile.objects.all()
    # permission_classes = [IsAuthenticated]


# *** Staff (Profile ID) -> [GET, PUT, PATCH, DELETE] *** #
# class StaffProfileView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = serializers.StaffProfileSerializer
#     # permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return models.StaffProfile.objects.all()

#     def get_object(self):
#         try:
#             staff_pk = self.kwargs["pk"]  # 1
#             staff_profile = models.StaffProfile.objects.get(user=staff_pk)
#             return staff_profile
#         except models.StaffProfile.DoesNotExist:
#             status_code = status.HTTP_404_NOT_FOUND
#             raise NotFound(
#                 {
#                     "success": "False",
#                     "code": 1,
#                     "message": "Staff Profile not found",
#                     "status_code": status_code,
#                     "data": "",
#                 }
#             )

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         staff_data = serializer.data

#         if staff_data["user"]["is_staff"] == False:
#             message = "Staff Profile whit this id is not Found."
#             return utils.FunReturn(
#                 1,
#                 message,
#                 status.HTTP_404_NOT_FOUND,
#             )

#         message = "Staff Profile retrieved Successfully."
#         return utils.FunReturn(
#             0,
#             message,
#             status.HTTP_200_OK,
#             staff_data,
#         )

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop("partial", False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         staff_data = serializer.data
#         message = "Staff Profile updated Successfully."
#         return utils.FunReturn(
#             0,
#             message,
#             status.HTTP_200_OK,
#             staff_data,
#         )


# *** Staff (Resend OTP) -> [POST] *** # 
class StaffResendOTPView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.StaffResendOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        try:
            user = models.User.objects.get(email=email)
            if user.is_verified:
                message = "Your account has already been verified. Please go to the login page."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN)

            utils.send_otp_for_user(user.email, "staff")
        except models.User.DoesNotExist:
            message = "No user found with this email."
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)

        message = "OTP has been resent to your email."
        return utils.FunReturn(0, message, status.HTTP_200_OK)


# *** Staff (Verify Account) -> [POST] *** # 
class StaffVerifyAccountView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.StaffVerifyAccountSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        otp_code = serializer.validated_data["otp_code"]
        try:
            otp = models.OneTimeOTP.objects.get(otp=otp_code)
        except models.OneTimeOTP.DoesNotExist:
            message = "Invalid OTP Code"
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        if otp.is_expired():
            message = "OTP has expired"
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        if otp.user:
            user = otp.user
        else:
            message = "No associated user for this OTP code"
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        if user.is_verified:
            message = "Email already verified"
            staff_data = serializers.UserSerializer(user).data
            return utils.FunReturn(0, message, status.HTTP_200_OK, staff_data)

        user.is_verified = True
        user.save()
        utils.send_verification_email(user, otp_code)
        otp.delete()
        staff_data = serializers.UserSerializer(user).data
        message = "Email verified Successfully."
        return utils.FunReturn(0, message, status.HTTP_200_OK, staff_data)


# *** Staff (Login) -> [POST] *** # 
class StaffLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.StaffLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            staff = serializer.validated_data

            if not staff.is_verified:
                message = "Your account is not verified. Please verify your account to proceed."
                return utils.FunReturn(
                    1, 
                    message, 
                    status.HTTP_403_FORBIDDEN, 
                    serializer.validated_data,
                )

            refresh = RefreshToken.for_user(staff)
            refresh["staff_id"] = staff.id
            access_token = refresh.access_token

            try:
                staff_profile = models.StaffProfile.objects.get(user=staff)
                staff_profile_data = serializers.StaffProfileSerializer(staff_profile).data
            except models.StaffProfile.DoesNotExist:
                staff_profile_data = None

            staff_data = serializers.UserSerializer(staff).data
            response = {
                "success": "True",
                "code": 0,
                "message": "Staff Login Successfully.",
                "status_code": status.HTTP_200_OK,
                "data": staff_data,
                "profile": staff_profile_data,
                "access_token": str(access_token),
                "refresh_token": str(refresh),
            }
            return Response(response, status=status.HTTP_200_OK)
        return utils.FunReturn(
            1, 
            serializer.errors, 
            status.HTTP_400_BAD_REQUEST,
        )


# *** Staff (Refresh) -> [POST] *** # 
class StaffRefreshView(generics.GenericAPIView):
    serializer_class = serializers.StaffRefreshSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data["refresh_token"]
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                message = {"refresh_token": "Invalid token payload."}
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

            staff = models.User.objects.get(id=user_id)
            staff_data = serializers.UserSerializer(staff).data
            message = "Staff retrieved Successfully."
            return utils.FunReturn(0, message, status.HTTP_200_OK, staff_data)
        except models.User.DoesNotExist:
            message = {"message": "Staff not found."}
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            message = {"message": "Refresh token has expired."}
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            message = {"message": "Invalid refresh token."}
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            message = {"message": str(e)}
            return utils.FunReturn(1, message, status.HTTP_500_INTERNAL_SERVER_ERROR)


# *** Staff (Change Password) -> [POST] *** # 
class StaffChangePasswordView(generics.GenericAPIView):
    serializer_class = serializers.StaffChangePasswordSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data["refresh_token"]
        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]
        confirm_password = serializer.validated_data["confirm_password"]

        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
            staff_id = payload.get("staff_id")
            staff = models.User.objects.get(id=staff_id)

            if not check_password(old_password, staff.password):
                message = "Old password is incorrect."
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_password:
                message = "New passwords do not match."
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

            staff.set_password(new_password)
            staff.save()
            utils.send_change_password_confirm(staff)
            staff_data = serializers.UserSerializer(staff).data
            message = "Password changed Successfully."
            return utils.FunReturn(0, message, status.HTTP_200_OK, staff_data)
        except jwt.ExpiredSignatureError:
            message = "Token has expired"
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            message = "Invalid token"
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except models.User.DoesNotExist:
            message = "Staff not found"
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)
        

# *** Staff (Logout) -> [POST] *** # 
class StaffLogoutView(generics.GenericAPIView):
    serializer_class = serializers.StaffLogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data["refresh_token"]
        try:
            token = RefreshToken(refresh_token)
            staff_id_in_token = token.payload.get("user_id")
            if not staff_id_in_token:
                message = "Invalid token: user id missing."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN)

            staff = models.User.objects.filter(id=staff_id_in_token).first()
            if not staff:
                message = "Invalid token: staff not found."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN)

            # token.blacklist()  # بدلاً من token.set_exp()
            token.set_exp()
            message = "Logout Successful."
            return utils.FunReturn(0, message, status.HTTP_200_OK)
        except Exception as e:
            message = str(e)
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)
        

# *** Staff (Reset Password) -> [POST] *** # 
class StaffPasswordResetView(generics.GenericAPIView):
    serializer_class = serializers.StaffPasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        try:
            staff = models.User.objects.get(email=email)
            staff_data = serializers.UserSerializer(staff).data
            if not staff.is_verified:
                message = "Your account is not verified. Please verify your account to proceed."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN, staff_data)
        except models.User.DoesNotExist:
            message = "Staff with this email does not exist."
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        try:
            utils.send_otp_for_password_reset(email, user_type="staff")
            message = "OTP has been sent to your email."
            return utils.FunReturn(0, message, status.HTTP_200_OK, staff_data)
        except ValueError as e:
            message = str(e)
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)


# *** Staff (Confirm Reset Password) -> [POST] *** # 
class StaffConfirmResetPasswordView(generics.GenericAPIView):
    serializer_class = serializers.StaffConfirmResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        otp = serializer.validated_data["otp"]
        password = serializer.validated_data["password"]

        try:
            otp_instance = models.OneTimeOTP.objects.get(otp=otp, user__isnull=False)
            if otp_instance.is_expired():
                message = "OTP has expired."
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)
        except models.OneTimeOTP.DoesNotExist:
            message = "Invalid OTP."
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        staff = otp_instance.user
        staff.set_password(password)
        staff.save()
        utils.send_reset_password_confirm(staff)
        models.OneTimeOTP.objects.filter(user=staff).delete()
        staff_data = serializers.UserSerializer(staff).data
        message = "Confirm Reset Password Successfully."
        return utils.FunReturn(0, message, status.HTTP_200_OK, staff_data)


# *** Staff (Search) -> [GET] *** #
# class StaffsSearchList(generics.ListCreateAPIView):
#     queryset = models.User.objects.filter(is_staff=True)
#     serializer_class = serializers.UserSerializer
#     pagination_class = StandardResultSetPagination
#     # permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         qs = super().get_queryset()

#         if 'searchstring' in self.kwargs:
#             search = self.kwargs['searchstring'] 
#             qs = qs.filter(
#                 Q(full_name__icontains=search)
#                 |Q(username__icontains=search)
#                 |Q(email__icontains=search)
#                 )
#         return qs


# *** Staff (Search) -> [GET] *** #
class StaffsSearchList(generics.ListCreateAPIView):
    queryset = models.StaffProfile.objects.filter()
    serializer_class = serializers.StaffProfileSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring'] 
            qs = qs.filter(
                Q(user__full_name__icontains=search)
                |Q(user__username__icontains=search)
                |Q(user__email__icontains=search)
                )
        return qs






# ******************************************************************************
# ==============================================================================
# *** 4) Student *** #
# *** Student (Register) -> [POST] *** #
class StudentRegisterView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.StudentRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.StudentRegisterSerializer(data=request.data)

        if serializer.is_valid():
            # Step 1: Save the user data using the serializer's create method
            student = serializer.save()
            student_data = serializers.UserSerializer(student).data

            # Step 2: Send OTP to the student's email using the utility function
            try:
                # Call the email-sending function
                utils.send_otp_for_user(student.email, "student")
            except SMTPRecipientsRefused as e:
                # Handle invalid email error
                # error_messages = str(e.recipients)
                # print(f"Error sending OTP to {student.email}: {error_messages}")
                raise ValidationError(
                    {
                        "Error": f"Error sending OTP to {student.email}: {e}",
                    }
                )

            # Step 3: Return success response
            message = "Student registered Successfully, and We have sent an OTP to your Email!"
            return utils.FunReturn(
                0,
                message,
                status.HTTP_201_CREATED,
                student_data,
            )

        message = serializer.errors
        return utils.FunReturn(
            1,
            message,
            status.HTTP_400_BAD_REQUEST,
        )


# *** Student (Register Verify) -> [POST] *** #
class StudentRegisterVerifyView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.StudentRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.StudentRegisterSerializer(data=request.data)

        if serializer.is_valid():
            # Step 1: Save the user data using the serializer's create method
            student = serializer.save()
            student.is_verified = True
            student.save()
            student_data = serializers.UserSerializer(student).data


            # Step 2: Return success response
            message = "Student Registered Successfully."
            return utils.FunReturn(
                0,
                message,
                status.HTTP_201_CREATED,
                student_data,
            )

        # Step 3:
        message = serializer.errors
        return utils.FunReturn(
            1,
            message,
            status.HTTP_400_BAD_REQUEST,
        )


# *** Student (Students) -> [GET, POST] *** #
class StudentsListView(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_student=True)
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]


# *** Student (Students) -> [GET, POST] *** #
class StudentsListAdmin(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_student=True)
    permission_classes = [AllowAny]


# *** Student (Student ID) -> [GET, POST, PUT, DELETE] *** #
class StudentPKAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_student=True)
    # permission_classes = [IsAuthenticated]


# *** Student (ID) -> [GET] *** # 
class StudentIDView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserSerializer

    def get(self, request, pk):
        try:
            student = models.User.objects.get(pk=pk)
        except models.User.DoesNotExist:
            message = "Student not found."
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)

        student_data = self.get_serializer(student).data
        if student_data["is_student"] == False:
            message = "Student with this Id is not Found."
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)

        try:
            student_profile = models.StudentProfile.objects.get(user=student)
            student_profile_data = serializers.StudentProfileSerializer(student_profile).data
        except models.StudentProfile.DoesNotExist:
            student_profile_data = None

        message = "Student retrieved Successfully."
        return Response({
            "success": "True",
            "code": 0,
            "message": message,
            "status_code": status.HTTP_200_OK,
            "data": student_data,
            "profile": student_profile_data,
        }, status.HTTP_200_OK)
    

# *** Student (Profiles) -> [GET, POST] *** #
class StudentProfileList(generics.ListCreateAPIView):
    serializer_class = serializers.StudentProfileSerializer
    queryset = models.StudentProfile.objects.all()
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]


# *** Student (Profile ID) -> [GET, PUT, PATCH, DELETE] *** #
class StudentProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.StudentProfileSerializer
    queryset = models.StudentProfile.objects.all()
    # permission_classes = [IsAuthenticated]


# *** Student (Profile ID) -> [GET, PUT, PATCH, DELETE] *** #
# class StudentProfileView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = serializers.StudentProfileSerializer
#     # permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return models.StudentProfile.objects.all()

#     def get_object(self):
#         try:
#             student_pk = self.kwargs["pk"]  # 1
#             student_profile = models.StudentProfile.objects.get(user=student_pk)
#             return student_profile
#         except models.StudentProfile.DoesNotExist:
#             status_code = status.HTTP_404_NOT_FOUND
#             raise NotFound(
#                 {
#                     "success": "False",
#                     "code": 1,
#                     "message": "Student Profile not found",
#                     "status_code": status_code,
#                     "data": "",
#                 }
#             )

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         student_data = serializer.data

#         if student_data["user"]["is_student"] == False:
#             message = "Student Profile whit this id is not Found."
#             return utils.FunReturn(
#                 1,
#                 message,
#                 status.HTTP_404_NOT_FOUND,
#             )

#         message = "Student Profile retrieved Successfully."
#         return utils.FunReturn(
#             0,
#             message,
#             status.HTTP_200_OK,
#             student_data,
#         )

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop("partial", False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         student_data = serializer.data
#         message = "Student Profile updated Successfully."
#         return utils.FunReturn(
#             0,
#             message,
#             status.HTTP_200_OK,
#             student_data,
#         )


# *** Student (Resend OTP) -> [POST] *** # 
class StudentResendOTPView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.StudentResendOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        try:
            user = models.User.objects.get(email=email)
            if user.is_verified:
                message = "Your account has already been verified. Please go to the login page."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN)

            utils.send_otp_for_user(user.email, "student")
        except models.User.DoesNotExist:
            message = "No user found with this email."
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)

        message = "OTP has been resent to your email."
        return utils.FunReturn(0, message, status.HTTP_200_OK)


# *** Student (Verify Account) -> [POST] *** # 
class StudentVerifyAccountView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.StudentVerifyAccountSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        otp_code = serializer.validated_data["otp_code"]
        try:
            otp = models.OneTimeOTP.objects.get(otp=otp_code)
        except models.OneTimeOTP.DoesNotExist:
            message = "Invalid OTP Code"
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        if otp.is_expired():
            message = "OTP has expired"
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        if otp.user:
            user = otp.user
        else:
            message = "No associated user for this OTP code"
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        if user.is_verified:
            message = "Email already verified"
            student_data = serializers.UserSerializer(user).data
            return utils.FunReturn(0, message, status.HTTP_200_OK, student_data)

        user.is_verified = True
        user.save()
        utils.send_verification_email(user, otp_code)
        otp.delete()
        student_data = serializers.UserSerializer(user).data
        message = "Email verified Successfully."
        return utils.FunReturn(0, message, status.HTTP_200_OK, student_data)
    

# *** Student (Login) -> [POST] *** #
class StudentLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.StudentLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            student = serializer.validated_data
            if not student.is_verified:
                message = "Your account is not verified. Please verify your account to proceed."
                return utils.FunReturn(
                    1, 
                    message, 
                    status.HTTP_403_FORBIDDEN, 
                    serializer.validated_data,
                )

            refresh = RefreshToken.for_user(student)
            refresh["student_id"] = student.id
            access_token = refresh.access_token

            try:
                student_profile = models.StudentProfile.objects.get(user=student)
                student_profile_data = serializers.StudentProfileSerializer(student_profile).data
            except models.StudentProfile.DoesNotExist:
                student_profile_data = None

            student_data = serializers.UserSerializer(student).data
            response = {
                "success": "True",
                "code": 0,
                "message": "Student Login Successfully.",
                "status_code": status.HTTP_200_OK,
                "data": student_data,
                "profile": student_profile_data,
                "access_token": str(access_token),
                "refresh_token": str(refresh),
            }
            return Response(response, status=status.HTTP_200_OK)
        return utils.FunReturn(
            1, 
            serializer.errors, 
            status.HTTP_400_BAD_REQUEST,
            )


# *** Student (Refresh) -> [POST] *** # 
class StudentRefreshView(generics.GenericAPIView):
    serializer_class = serializers.StudentRefreshSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data["refresh_token"]
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                message = {"refresh_token": "Invalid token payload."}
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

            student = models.User.objects.get(id=user_id)
            student_data = serializers.UserSerializer(student).data
            message = "Student retrieved Successfully."
            return utils.FunReturn(0, message, status.HTTP_200_OK, student_data)
        except models.User.DoesNotExist:
            message = {"message": "Student not found."}
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            message = {"message": "Refresh token has expired."}
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            message = {"message": "Invalid refresh token."}
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            message = {"message": str(e)}
            return utils.FunReturn(1, message, status.HTTP_500_INTERNAL_SERVER_ERROR)


# *** Student (Change Password) -> [POST] *** # 
class StudentChangePasswordView(generics.GenericAPIView):
    serializer_class = serializers.StudentChangePasswordSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data["refresh_token"]
        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]
        confirm_password = serializer.validated_data["confirm_password"]

        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
            student_id = payload.get("user_id")
            student = models.User.objects.get(id=student_id)

            if not check_password(old_password, student.password):
                message = "Old password is incorrect."
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_password:
                message = "New passwords do not match."
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

            student.set_password(new_password)
            student.save()
            utils.send_change_password_confirm(student)
            student_data = serializers.UserSerializer(student).data
            message = "Password changed successfully."
            return utils.FunReturn(0, message, status.HTTP_200_OK, student_data)
        except jwt.ExpiredSignatureError:
            message = "Token has expired"
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            message = "Invalid token"
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except models.User.DoesNotExist:
            message = "Student not found"
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)


# *** Student (Logout) -> [POST] *** # 
class StudentLogoutView(generics.GenericAPIView):
    serializer_class = serializers.StudentLogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data["refresh_token"]
        try:
            token = RefreshToken(refresh_token)
            student_id_in_token = token.payload.get("user_id")
            if not student_id_in_token:
                message = "Invalid token: user id missing."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN)

            student = models.User.objects.filter(id=student_id_in_token).first()
            if not student:
                message = "Invalid token: student not found."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN)

            # token.blacklist()  # بدلاً من token.set_exp()
            token.set_exp()
            message = "Logout Successful."
            return utils.FunReturn(0, message, status.HTTP_200_OK)
        except Exception as e:
            message = str(e)
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)


# *** Student (Reset Password) -> [POST] *** #
class StudentPasswordResetView(generics.GenericAPIView):
    serializer_class = serializers.StudentPasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        try:
            student = models.User.objects.get(email=email)
            student_data = serializers.UserSerializer(student).data
            if not student.is_verified:
                message = "Your account is not verified. Please verify your account to proceed."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN, student_data)
        except models.User.DoesNotExist:
            message = "Student with this email does not exist."
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        try:
            utils.send_otp_for_password_reset(email, user_type="student")
            message = "OTP has been sent to your email."
            return utils.FunReturn(0, message, status.HTTP_200_OK, student_data)
        except ValueError as e:
            message = str(e)
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)


# *** Student (Confirm Reset Password) -> [POST] *** # 
class StudentConfirmResetPasswordView(generics.GenericAPIView):
    serializer_class = serializers.StudentConfirmResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        otp = serializer.validated_data["otp"]
        password = serializer.validated_data["password"]

        try:
            otp_instance = models.OneTimeOTP.objects.get(otp=otp, user__isnull=False)
            if otp_instance.is_expired():
                message = "OTP has expired."
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)
        except models.OneTimeOTP.DoesNotExist:
            message = "Invalid OTP."
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        student = otp_instance.user
        student.set_password(password)
        student.save()
        utils.send_reset_password_confirm(student)
        models.OneTimeOTP.objects.filter(user=student).delete()
        student_data = serializers.UserSerializer(student).data
        message = "Confirm Reset Password Successfully."
        return utils.FunReturn(0, message, status.HTTP_200_OK, student_data)


# *** Student (Search) -> [GET] *** #
# class StudentsSearchList(generics.ListCreateAPIView):
#     queryset = models.User.objects.filter(is_student=True)
#     serializer_class = serializers.UserSerializer
#     pagination_class = StandardResultSetPagination
#     # permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         qs = super().get_queryset()

#         if 'searchstring' in self.kwargs:
#             search = self.kwargs['searchstring'] 
#             qs = qs.filter(
#                 Q(full_name__icontains=search)
#                 |Q(username__icontains=search)
#                 |Q(email__icontains=search)
#                 )
#         return qs



# *** Student (Search) -> [GET] *** #
class StudentsSearchList(generics.ListCreateAPIView):
    queryset = models.StudentProfile.objects.filter()
    serializer_class = serializers.StudentProfileSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring'] 
            qs = qs.filter(
                Q(user__full_name__icontains=search)
                |Q(user__username__icontains=search)
                |Q(user__email__icontains=search)
                )
        return qs






# ******************************************************************************
# ==============================================================================
# *** 5) Public *** #
# *** User (Users) -> [GET, POST] *** #
class PublicUsersListView(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]


# *** User (User ID) -> [GET, POST, PUT, DELETE] *** #
class PublicUserPKAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    # permission_classes = [IsAuthenticated]


# *** Public (Login) -> [POST] *** #
class PublicLoginView(generics.GenericAPIView):
    serializer_class = serializers.PublicLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data
        user_data = serializers.UserSerializer(user).data

        if not user.is_verified:
            message = "Your account is not verified. Please verify your account to proceed."
            return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN, user_data)

        profile = None
        if user_data["is_admin"]:
            profile = models.AdminProfile.objects.get(user=user_data["id"])
            user_profile = serializers.AdminProfileSerializer(profile).data
        elif user_data["is_teacher"]:
            profile = models.TeacherProfile.objects.get(user=user_data["id"])
            user_profile = serializers.TeacherProfileSerializer(profile).data
        elif user_data["is_staff"]:
            profile = models.StaffProfile.objects.get(user=user_data["id"])
            user_profile = serializers.StaffProfileSerializer(profile).data
        elif user_data["is_student"]:
            profile = models.StudentProfile.objects.get(user=user_data["id"])
            user_profile = serializers.StudentProfileSerializer(profile).data

        refresh = RefreshToken.for_user(user)
        refresh["user_id"] = user.id
        access_token = refresh.access_token

        response = {
            "success": True,
            "code": 0,
            "message": "User Login Successfully.",
            "status_code": status.HTTP_200_OK,
            "data": user_data,
            "profile": user_profile,
            "access_token": str(access_token),
            "refresh_token": str(refresh),
        }
        return Response(response, status=status.HTTP_200_OK)


# *** Public (ID) -> [GET] *** #
class PublicIDView(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer

    def get(self, request, pk):
        try:
            user = models.User.objects.get(pk=pk)
        except models.User.DoesNotExist:
            message = "User not found."
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)

        user_data = self.get_serializer(user).data
        user_profile = ""

        # إذا كنت ترغب في جلب بيانات الملف الشخصي للمستخدم
        if user.is_admin:
            profile = models.AdminProfile.objects.get(user=user)
            user_profile = serializers.AdminProfileSerializer(profile).data
        elif user.is_superuser:
            profile = models.SuperuserProfile.objects.get(user=user)
            user_profile = serializers.SuperuserProfileSerializer(profile).data
        elif user.is_teacher:
            profile = models.TeacherProfile.objects.get(user=user)
            user_profile = serializers.TeacherProfileSerializer(profile).data
        elif user.is_staff:
            profile = models.StaffProfile.objects.get(user=user)
            user_profile = serializers.StaffProfileSerializer(profile).data
        elif user.is_student:
            profile = models.StudentProfile.objects.get(user=user)
            user_profile = serializers.StudentProfileSerializer(profile).data
        else:
            user_profile = ""

        response = {
            "success": True,
            "code": 0,
            "message": "User Retrieved Successfully.",
            "status_code": status.HTTP_200_OK,
            "data": user_data,
            "profile": user_profile,
        }
        return Response(response, status.HTTP_200_OK)


# *** Public (ID) -> [GET] *** #
class PublicVerifyAccountView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.PublicVerifyAccountSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        otp_code = serializer.validated_data["otp_code"]
        try:
            otp = models.OneTimeOTP.objects.get(otp=otp_code)
        except models.OneTimeOTP.DoesNotExist:
            message = "Invalid OTP Code"
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        if otp.is_expired():
            message = "OTP has expired"
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        if otp.user:
            user = otp.user
        else:
            message = "No associated user for this OTP code"
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        if user.is_verified:
            message = "Email already verified"
            student_data = serializers.UserSerializer(user).data
            return utils.FunReturn(0, message, status.HTTP_200_OK, student_data)

        user.is_verified = True
        user.save()
        utils.send_verification_email(user, otp_code)
        otp.delete()
        student_data = serializers.UserSerializer(user).data
        message = "Email verified Successfully."
        return utils.FunReturn(0, message, status.HTTP_200_OK, student_data)


# *** Public (Resend OTP) -> [POST] *** # 
class PublicResendOTPView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.PublicResendOTPSerializer
        
    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        try:
            user = models.User.objects.get(email=email)
            if user.is_verified:
                message = "Your account has already been verified. Please go to the login page."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN)

            utils.send_otp_for_user(user.email, "user")
        except models.User.DoesNotExist:
            message = "No user found with this email."
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)

        message = "OTP has been resent to your email."
        return utils.FunReturn(0, message, status.HTTP_200_OK)


# *** Public (Refresh) -> [POST] *** # 
class PublicRefreshView(generics.GenericAPIView):
    serializer_class = serializers.PublicRefreshSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data["refresh_token"]
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            if not user_id:
                message = {"refresh_token": "Invalid token payload."}
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

            user = models.User.objects.get(id=user_id)
            user_data = serializers.UserSerializer(user).data
            message = "User retrieved Successfully."
            return utils.FunReturn(0, message, status.HTTP_200_OK, user_data)
        except models.User.DoesNotExist:
            message = {"message": "User not found."}
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            message = {"message": "Refresh token has expired."}
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            message = {"message": "Invalid refresh token."}
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            message = {"message": str(e)}
            return utils.FunReturn(1, message, status.HTTP_500_INTERNAL_SERVER_ERROR)



# *** Public (Change Password) -> [POST] *** # 
class PublicChangePasswordView(generics.GenericAPIView):
    serializer_class = serializers.PublicChangePasswordSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data["refresh_token"]
        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]
        confirm_password = serializer.validated_data["confirm_password"]

        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            user = models.User.objects.get(id=user_id)

            if not check_password(old_password, user.password):
                message = "Old password is incorrect."
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_password:
                message = "New passwords do not match."
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            utils.send_change_password_confirm(user)
            user_data = serializers.UserSerializer(user).data
            message = "Password changed successfully."
            return utils.FunReturn(0, message, status.HTTP_200_OK, user_data)
        except jwt.ExpiredSignatureError:
            message = "Token has expired"
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            message = "Invalid token"
            return utils.FunReturn(1, message, status.HTTP_401_UNAUTHORIZED)
        except models.User.DoesNotExist:
            message = "User not found"
            return utils.FunReturn(1, message, status.HTTP_404_NOT_FOUND)

# *** Public (Logout) -> [POST] *** # 
class PublicLogoutView(generics.GenericAPIView):
    serializer_class = serializers.PublicLogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data["refresh_token"]
        try:
            token = RefreshToken(refresh_token)
            user_id_in_token = token.payload.get("user_id")

            if not user_id_in_token:
                message = "Invalid token: user id missing."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN)

            user = models.User.objects.filter(id=user_id_in_token).first()
            if not user:
                message = "Invalid token: User not found."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN)

            # token.blacklist()  # بدلاً من token.set_exp()
            token.set_exp()
            message = "Logout Successful."
            return utils.FunReturn(0, message, status.HTTP_200_OK)
        except Exception as e:
            message = str(e)
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)


# *** Public (Reset Password) -> [POST] *** #
class PublicPasswordResetView(generics.GenericAPIView):
    serializer_class = serializers.PublicPasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        try:
            user = models.User.objects.get(email=email)
            user_data = serializers.UserSerializer(user).data

            if not user.is_verified:
                message = "Your account is not verified. Please verify your account to proceed."
                return utils.FunReturn(1, message, status.HTTP_403_FORBIDDEN, user_data)
        except models.User.DoesNotExist:
            message = "User with this email does not exist."
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        try:
            utils.send_otp_for_password_reset(email, user_type="user")
            message = "OTP has been sent to your email."
            return utils.FunReturn(0, message, status.HTTP_200_OK, user_data)
        except ValueError as e:
            message = str(e)
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)


# *** Public (Confirm Reset Password) -> [POST] *** # 
class PublicConfirmResetPasswordView(generics.GenericAPIView):
    serializer_class = serializers.PublicConfirmResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        otp = serializer.validated_data["otp"]
        password = serializer.validated_data["password"]

        try:
            otp_instance = models.OneTimeOTP.objects.get(otp=otp, user__isnull=False)
            if otp_instance.is_expired():
                message = "OTP has expired."
                return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)
        except models.OneTimeOTP.DoesNotExist:
            message = "Invalid OTP."
            return utils.FunReturn(1, message, status.HTTP_400_BAD_REQUEST)

        user = otp_instance.user
        user.set_password(password)
        user.save()
        utils.send_reset_password_confirm(user)
        models.OneTimeOTP.objects.filter(user=user).delete()
        user_data = serializers.UserSerializer(user).data
        message = "Confirm Reset Password Successfully."
        return utils.FunReturn(0, message, status.HTTP_200_OK, user_data)


# *** Public (Search) -> [GET] *** #
class PublicUserSearchList(generics.ListCreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    pagination_class = StandardResultSetPagination
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()

        if 'searchstring' in self.kwargs:
            search = self.kwargs['searchstring'] 
            qs = qs.filter(
                Q(full_name__icontains=search)
                |Q(username__icontains=search)
                |Q(email__icontains=search)
                )
        return qs




# *****************************************************************
# =================================================================