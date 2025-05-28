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


SECRET_KEY = settings.SECRET_KEY


#
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


#
from accounts import models
from accounts import serializers
from accounts import utils






# ******************************************************************************
# ==============================================================================
# *** 1) Admin *** #
# *** Admin (Register) *** #
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

# *** Admin (Register Verify) *** #
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


# *** Admin (Admins) *** #
class AdminsListView(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_admin=True)


# *** Admin (Admin ID) -> [GET, POST, PUT, DELETE] *** #
class AdminPKAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_admin=True)


# *** Admin (Profile) *** #
class AdminProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AdminProfileSerializer

    def get_queryset(self):
        return models.AdminProfile.objects.all()

    def get_object(self):
        try:
            admin_pk = self.kwargs["pk"]  # 1
            admin_profile = models.AdminProfile.objects.get(user=admin_pk)
            return admin_profile
        except models.AdminProfile.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            raise NotFound(
                {
                    "success": "False",
                    "code": 1,
                    "message": "Admin Profile not found.",
                    "status_code": status_code,
                    "data": "",
                }
            )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        admin_data = serializer.data

        if admin_data["admin"]["is_admin"] == False:
            message = "Admin Profile whit this id is not Found."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_404_NOT_FOUND,
            )

        message = "Admin Profile retrieved Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            admin_data,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        admin_data = serializer.data
        message = "Admin Profile updated Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            admin_data,
        )


# *** Admin (Resend OTP) *** #
class AdminResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.AdminResendOTPSerializer(data=request.data)

        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data["email"]
        try:
            user = models.User.objects.get(email=email)

            # Check if the teacher is already verified
            if user.is_verified:
                message = "Your account has already been verified. Please go to the login page."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                )

            # Resend OTP if not verified
            utils.send_otp_for_user(user.email, "admin")
        except models.User.DoesNotExist:
            message = "No user found with this email."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_404_NOT_FOUND,
            )

        message = "OTP has been resent to your email."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
        )


# *** Admin (Verify Account) *** #
class AdminVerifyAccountView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        otp_code = request.data.get("otp_code")

        # Ensure OTP code is provided
        if not otp_code:
            message = "OTP code is required"
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Retrieve the OTP record from OneTimeOTP model
            otp = models.OneTimeOTP.objects.get(otp=otp_code)
        except models.OneTimeOTP.DoesNotExist:
            message = "Invalid OTP Code"
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Check OTP expiration
        if otp.is_expired():
            message = "OTP has expired"
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Determine if the OTP belongs to a User
        if otp.user:
            user = otp.user
        else:
            message = "No associated user for this OTP code"
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Check if the user is already verified
        if user.is_verified:
            message = "Email already verified"
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
            )

        # Mark user as verified
        user.is_verified = True
        user.save()

        # Send verification success email
        utils.send_verification_email(
            user, otp_code
        )  # Assuming this sends the confirmation email

        # Optionally delete OTP record after successful verification
        otp.delete()

        teacher_data = serializers.UserSerializer(user).data
        message = "Email verified Successfully"
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            teacher_data,
        )


# *** Admin (Login) *** #
class AdminLoginView(APIView):
    def post(self, request):
        # Deserialize the admin login data
        serializer = serializers.AdminLoginSerializer(data=request.data)

        if serializer.is_valid():
            admin = serializer.validated_data  # Extract the validated admin
            admin_data = serializers.UserSerializer(admin).data

            if not admin.is_verified:
                message = "Your account is not verified. Please verify your account to proceed."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                    admin_data,
                )

            # Generate refresh token and include admin_id in the token payload
            refresh = RefreshToken.for_user(admin)
            refresh["admin_id"] = (
                admin.id
            )  # Explicitly add admin_id to the token payload

            # Generate access token
            access_token = refresh.access_token

            admin_data = serializers.UserSerializer(admin).data
            status_code = status.HTTP_200_OK
            response = {
                "success": "True",
                "code": 0,
                "message": "Admin Login Successfully.",
                "status_code": status_code,
                "data": admin_data,
                "access_token": str(access_token),
                "refresh_token": str(refresh),
            }
            return Response(
                response,
                status=status_code,
            )

        message = serializer.errors
        return utils.FunReturn(
            1,
            message,
            status.HTTP_400_BAD_REQUEST,
        )


# *** Admin (ID) *** #
class AdminIDView(APIView):
    def get(self, request, pk):
        try:
            admin = models.User.objects.get(pk=pk)
        except models.User.DoesNotExist:
            message = "Admin not found."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_404_NOT_FOUND,
            )

        admin_data = serializers.UserSerializer(admin).data

        if admin_data["is_admin"] == False:
            message = "Admin whit this id is not Found."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_404_NOT_FOUND,
            )

        message = "Admin retrieved Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            admin_data,
        )


# *** Admin (Refresh) *** #
class AdminRefreshView(APIView):
    def post(self, request):
        try:
            # Retrieve and decode the refresh token
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                message = {
                    "refresh_token": "This field is required.",
                }
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_400_BAD_REQUEST,
                )

            # Decode the JWT token
            payload = jwt.decode(
                refresh_token, SECRET_KEY, algorithms=["HS256"]
            )  # {'token_type': 'refresh', 'exp': 1737402322, 'iat': 1737315922, 'jti': '626f3935d64e4ebcbfcb53d54041f2ab', 'user_id': 1, 'teacher_id': 1}

            # Retrieve user_id from the token payload
            user_id = payload.get("user_id")
            if not user_id:
                raise ValidationError(
                    {
                        "refresh_token": "Invalid token payload.",
                    }
                )

            # Fetch the Admin object
            admin = models.User.objects.get(id=user_id)

            # Serialize the Admin object
            admin_data = serializers.UserSerializer(admin).data
            message = "Admin retrieved successfully."
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
                admin_data,
            )

        except models.User.DoesNotExist:
            raise ValidationError(
                {
                    "message": "Admin not found.",
                }
            )

        except jwt.ExpiredSignatureError:
            raise ValidationError(
                {
                    "message": "Refresh token has expired.",
                }
            )

        except jwt.InvalidTokenError:
            raise ValidationError(
                {
                    "message": "Invalid refresh token.",
                }
            )

        except Exception as e:
            raise ValidationError(
                {
                    "message": str(e),
                }
            )


# *** Admin (Change Password) *** #
class AdminChangePasswordView(APIView):
    def post(self, request):
        try:
            # Retrieve and decode the refresh token
            refresh_token = request.data.get("refresh_token")

            if not refresh_token:
                raise ValidationError({"refresh_token": "This field is required."})

            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
            admin_id = payload.get("admin_id")

            # Fetch the admin
            admin = models.User.objects.get(id=admin_id)

            # Validate old password
            old_password = request.data.get("old_password")

            if not old_password or not check_password(old_password, admin.password):
                raise ValidationError({"message": "Old password is incorrect."})

            # Validate new passwords
            new_password = request.data.get("new_password")
            confirm_password = request.data.get("confirm_password")

            # validate_password(new_password, confirm_password)

            # Change password
            admin.set_password(new_password)
            admin.save()
            utils.send_change_password_confirm(admin)

            admin_data = serializers.UserSerializer(admin).data
            message = "Password changed successfully."
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
                admin_data,
            )

        except jwt.ExpiredSignatureError:
            raise ValidationError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValidationError("Invalid token")
        except models.User.DoesNotExist:
            raise ValidationError("Admin not found")
        except ValidationError as e:
            message = e.detail
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )


# *** Admin (Logout) *** #
class AdminLogoutView(APIView):
    def post(self, request):
        try:
            # Get the refresh token from the request
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                message = "Refresh token not provided."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_400_BAD_REQUEST,
                )

            # Decode the refresh token
            token = RefreshToken(refresh_token)
            admin_id_in_token = token.payload.get("user_id")

            if not admin_id_in_token:
                message = "Invalid token: user id missing."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                )

            # Validate that the admin exists and matches the current authenticated admin
            admin = models.User.objects.filter(id=admin_id_in_token).first()
            if not admin:
                message = "Invalid token: admin not found."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                )

            # Expire the token (logout the admin)
            token.set_exp()

            message = "Logout successful."
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
            )
        except Exception as e:
            message = str(e)
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )


# *** Admin (Reset Password) *** #
class AdminPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            message = "Email is required."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        try:
            admin = models.User.objects.get(email=email)
            admin_data = serializers.UserSerializer(admin).data

            if not admin.is_verified:
                message = "Your account is not verified. Please verify your account to proceed."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                    admin_data,
                )

        except models.User.DoesNotExist:
            message = "Admin with this email does not exist."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Send OTP for password reset
        try:
            utils.send_otp_for_password_reset(email, user_type="admin")
            message = "OTP has been sent to your email."
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
            )
        except ValueError as e:
            message = str(e)
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )


# *** Admin (Confirm Reset Password) *** #
class AdminConfirmResetPasswordView(APIView):
    """
    This view allows a Admin to reset their password after OTP verification.
    """

    def post(self, request):
        otp = request.data.get("otp")
        password = request.data.get("password")
        password2 = request.data.get("password2")

        if password != password2:
            message = "Passwords do not match."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Validate OTP
        try:
            otp_instance = models.OneTimeOTP.objects.get(otp=otp, user__isnull=False)
        except models.OneTimeOTP.DoesNotExist:
            message = "Invalid OTP."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        if otp_instance.is_expired():
            message = "OTP has expired."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        admin = otp_instance.user
        password = password

        admin.set_password(password)
        admin.save()
        utils.send_reset_password_confirm(admin)

        # Delete the used OTP
        models.OneTimeOTP.objects.filter(user=admin).delete()

        admin_data = serializers.UserSerializer(admin).data
        message = "Confirm Reset Password Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            admin_data,
        )










# ******************************************************************************
# ==============================================================================
# *** 2) Teacher *** #
# *** Teacher (Register) *** #
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

# *** Teacher (Register Verify) *** #
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


# *** Teacher (Teachers) *** #
class TeachersListView(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_teacher=True)


# *** Teacher (Teacher ID) -> [GET, POST, PUT, DELETE] *** #
class TeacherPKAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_teacher=True)


# *** Teacher (Profile) *** #
class TeacherProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TeacherProfileSerializer

    def get_queryset(self):
        return models.TeacherProfile.objects.all()

    def get_object(self):
        try:
            teacher_pk = self.kwargs["pk"]  # 1
            teacher_profile = models.TeacherProfile.objects.get(user=teacher_pk)
            return teacher_profile
        except models.TeacherProfile.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            raise NotFound(
                {
                    "success": "False",
                    "code": 1,
                    "message": "Teacher Profile not found",
                    "status_code": status_code,
                    "data": "",
                }
            )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        teacher_data = serializer.data

        if teacher_data["teacher"]["is_teacher"] == False:
            message = "Teacher Profile whit this id is not Found"
            return utils.FunReturn(
                1,
                message,
                status.HTTP_404_NOT_FOUND,
            )

        message = "Teacher Profile retrieved successfully"
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            teacher_data,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        teacher_data = serializer.data
        message = "Teacher Profile updated Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            teacher_data,
        )


# *** Teacher (Resend OTP) *** #
class TeacherResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.TeacherResendOTPSerializer(data=request.data)

        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data["email"]
        try:
            user = models.User.objects.get(email=email)

            # Check if the teacher is already verified
            if user.is_verified:
                message = "Your account has already been verified. Please go to the login page."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                )

            # Resend OTP if not verified
            utils.send_otp_for_user(user.email, "teacher")
        except models.User.DoesNotExist:
            message = "No user found with this email."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_404_NOT_FOUND,
            )

        message = "OTP has been resent to your email."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
        )


# *** Teacher (Verify Account) *** #
class TeacherVerifyAccountView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        otp_code = request.data.get("otp_code")

        # Ensure OTP code is provided
        if not otp_code:
            message = "OTP code is required"
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Retrieve the OTP record from OneTimeOTP model
            otp = models.OneTimeOTP.objects.get(otp=otp_code)
        except models.OneTimeOTP.DoesNotExist:
            message = "Invalid OTP Code"
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Check OTP expiration
        if otp.is_expired():
            message = "OTP has expired"
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Determine if the OTP belongs to a User
        if otp.user:
            user = otp.user
        else:
            message = "No associated user for this OTP code"
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Check if the user is already verified
        if user.is_verified:
            message = "Email already verified"
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
            )

        # Mark user as verified
        user.is_verified = True
        user.save()

        # Send verification success email
        utils.send_verification_email(
            user, otp_code
        )  # Assuming this sends the confirmation email

        # Optionally delete OTP record after successful verification
        otp.delete()

        teacher_data = serializers.UserSerializer(user).data
        message = "Email verified Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            teacher_data,
        )


# *** Teacher (Login) *** #
class TeacherLoginView(APIView):
    def post(self, request):
        # Deserialize the teacher login data
        serializer = serializers.TeacherLoginSerializer(data=request.data)

        if serializer.is_valid():
            teacher = serializer.validated_data  # Extract the validated teacher
            teacher_data = serializers.UserSerializer(teacher).data

            if not teacher.is_verified:
                message = "Your account is not verified. Please verify your account to proceed."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                    teacher_data,
                )

            # Generate refresh token and include teacher_id in the token payload
            refresh = RefreshToken.for_user(teacher)
            refresh["teacher_id"] = (
                teacher.id
            )  # Explicitly add teacher_id to the token payload

            # Generate access token
            access_token = refresh.access_token

            teacher_data = serializers.UserSerializer(teacher).data
            status_code = status.HTTP_200_OK
            response = {
                "success": "True",
                "code": 0,
                "message": "Teacher Login Successfully.",
                "status_code": status_code,
                "data": teacher_data,
                "access_token": str(access_token),
                "refresh_token": str(refresh),
            }
            return Response(
                response,
                status=status_code,
            )

        message = serializer.errors
        return utils.FunReturn(
            1,
            message,
            status.HTTP_400_BAD_REQUEST,
        )


# *** Teacher (ID) *** #
class TeacherIDView(APIView):
    def get(self, request, pk):
        try:
            teacher = models.User.objects.get(pk=pk)
        except models.User.DoesNotExist:
            message = "Teacher not found."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_404_NOT_FOUND,
            )

        teacher_data = serializers.UserSerializer(teacher).data

        if teacher_data["is_teacher"] == False:
            message = "Teacher with this Id is not Found."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_404_NOT_FOUND,
            )

        message = "Teacher retrieved Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            teacher_data,
        )


# *** Teacher (Refresh) *** #
class TeacherRefreshView(APIView):
    def post(self, request):
        try:
            # Retrieve and decode the refresh token
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                message = {
                    "refresh_token": "This field is required.",
                }
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_400_BAD_REQUEST,
                )

            # Decode the JWT token
            payload = jwt.decode(
                refresh_token, SECRET_KEY, algorithms=["HS256"]
            )  # {'token_type': 'refresh', 'exp': 1737402322, 'iat': 1737315922, 'jti': '626f3935d64e4ebcbfcb53d54041f2ab', 'user_id': 1, 'teacher_id': 1}

            # Retrieve user_id from the token payload
            user_id = payload.get("user_id")
            if not user_id:
                raise ValidationError(
                    {
                        "refresh_token": "Invalid token payload.",
                    }
                )

            # Fetch the Teacher object
            teacher = models.User.objects.get(id=user_id)

            # Serialize the Teacher object
            teacher_data = serializers.UserSerializer(teacher).data
            message = "Teacher retrieved Successfully."
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
                teacher_data,
            )

        except models.User.DoesNotExist:
            raise ValidationError(
                {
                    "message": "Teacher not found.",
                }
            )

        except jwt.ExpiredSignatureError:
            raise ValidationError(
                {
                    "message": "Refresh token has expired.",
                }
            )

        except jwt.InvalidTokenError:
            raise ValidationError(
                {
                    "message": "Invalid refresh token.",
                }
            )

        except Exception as e:
            raise ValidationError(
                {
                    "message": str(e),
                }
            )


# *** Teacher (Change Password) *** #
class TeacherChangePasswordView(APIView):
    def post(self, request):
        try:
            # Retrieve and decode the refresh token
            refresh_token = request.data.get("refresh_token")

            if not refresh_token:
                raise ValidationError({"refresh_token": "This field is required."})

            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
            teacher_id = payload.get("teacher_id")

            # Fetch the teacher
            teacher = models.User.objects.get(id=teacher_id)

            # Validate old password
            old_password = request.data.get("old_password")

            if not old_password or not check_password(old_password, teacher.password):
                raise ValidationError({"message": "Old password is incorrect."})

            # Validate new passwords
            new_password = request.data.get("new_password")
            confirm_password = request.data.get("confirm_password")

            # validate_password(new_password, confirm_password)

            # Change password
            teacher.set_password(new_password)
            teacher.save()
            utils.send_change_password_confirm(teacher)

            teacher_data = serializers.UserSerializer(teacher).data
            message = "Password changed successfully."
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
                teacher_data,
            )

        except jwt.ExpiredSignatureError:
            raise ValidationError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValidationError("Invalid token")
        except models.User.DoesNotExist:
            raise ValidationError("Teacher not found")
        except ValidationError as e:
            message = e.detail
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )


# *** Teacher (Logout) *** #
class TeacherLogoutView(APIView):
    def post(self, request):
        try:
            # Get the refresh token from the request
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                message = "Refresh token not provided."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_400_BAD_REQUEST,
                )

            # Decode the refresh token
            token = RefreshToken(refresh_token)
            teacher_id_in_token = token.payload.get("user_id")

            if not teacher_id_in_token:
                message = "Invalid token: user_id missing."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                )

            # Validate that the teacher exists and matches the current authenticated teacher
            teacher = models.User.objects.filter(id=teacher_id_in_token).first()
            if not teacher:
                message = "Invalid token: Teacher not found."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                )

            # Expire the token (logout the teacher)
            token.set_exp()
            message = "Logout Successful."
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
            )
        except Exception as e:
            message = str(e)
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )


# *** Teacher (Reset Password) *** #
class TeacherPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            message = "Email is required."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        try:
            teacher = models.User.objects.get(email=email)
            teacher_data = serializers.UserSerializer(teacher).data

            if not teacher.is_verified:
                message = "Your account is not verified. Please verify your account to proceed."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                    teacher_data,
                )

        except models.User.DoesNotExist:
            message = "Teacher with this email does not exist."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Send OTP for password reset
        try:
            utils.send_otp_for_password_reset(email, user_type="teacher")
            message = "OTP has been sent to your email."
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
            )
        except ValueError as e:
            message = str(e)
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )


# *** Teacher (Confirm Reset Password) *** #
class TeacherConfirmResetPasswordView(APIView):
    """
    This view allows a teacher to reset their password after OTP verification.
    """

    def post(self, request):
        otp = request.data.get("otp")
        password = request.data.get("password")
        password2 = request.data.get("password2")

        if password != password2:
            message = "Passwords do not match."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Validate OTP
        try:
            otp_instance = models.OneTimeOTP.objects.get(otp=otp, user__isnull=False)
        except models.OneTimeOTP.DoesNotExist:
            message = "Invalid OTP."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        if otp_instance.is_expired():
            message = "OTP has expired."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        teacher = otp_instance.user
        password = password

        teacher.set_password(password)
        teacher.save()
        utils.send_reset_password_confirm(teacher)

        # Delete the used OTP
        models.OneTimeOTP.objects.filter(user=teacher).delete()

        teacher_data = serializers.UserSerializer(teacher).data
        message = "Confirm Reset Password Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            teacher_data,
        )






# ******************************************************************************
# ==============================================================================
# *** 3) Staff *** #
# *** Staff (Register) *** #
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

# *** Staff (Register Verify) *** #
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


# *** Staff (Staffs) *** #
class StaffsListView(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_staff=True)

# *** Staff (Staff ID) -> [GET, POST, PUT, DELETE] *** #
class StaffPKAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_staff=True)


# *** Staff (Profile) *** #
class StaffProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.StaffProfileSerializer

    def get_queryset(self):
        return models.StaffProfile.objects.all()

    def get_object(self):
        try:
            staff_pk = self.kwargs["pk"]  # 1
            staff_profile = models.StaffProfile.objects.get(user=staff_pk)
            return staff_profile
        except models.StaffProfile.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            raise NotFound(
                {
                    "success": "False",
                    "code": 1,
                    "message": "Staff Profile not found",
                    "status_code": status_code,
                    "data": "",
                }
            )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        staff_data = serializer.data

        if staff_data["staff"]["is_staff"] == False:
            message = "Staff Profile whit this id is not Found."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_404_NOT_FOUND,
            )

        message = "Staff Profile retrieved Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            staff_data,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        staff_data = serializer.data
        message = "Staff Profile updated Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            staff_data,
        )


# *** Staff (Resend OTP) *** #
class StaffResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.StaffResendOTPSerializer(data=request.data)

        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data["email"]
        try:
            user = models.User.objects.get(email=email)

            # Check if the teacher is already verified
            if user.is_verified:
                message = "Your account has already been verified. Please go to the login page."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                )

            # Resend OTP if not verified
            utils.send_otp_for_user(user.email, "staff")
        except models.User.DoesNotExist:
            message = "No user found with this email."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_404_NOT_FOUND,
            )

        message = "OTP has been resent to your email."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
        )


# *** Staff (Verify Account) *** #
class StaffVerifyAccountView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        otp_code = request.data.get("otp_code")

        # Ensure OTP code is provided
        if not otp_code:
            message = "OTP code is required"
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Retrieve the OTP record from OneTimeOTP model
            otp = models.OneTimeOTP.objects.get(otp=otp_code)
        except models.OneTimeOTP.DoesNotExist:
            message = "Invalid OTP Code"
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Check OTP expiration
        if otp.is_expired():
            message = "OTP has expired"
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Determine if the OTP belongs to a User
        if otp.user:
            user = otp.user
        else:
            message = "No associated user for this OTP code"
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Check if the user is already verified
        if user.is_verified:
            message = "Email already verified"
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
                user,
            )

        # Mark user as verified
        user.is_verified = True
        user.save()

        # Send verification success email
        utils.send_verification_email(
            user, otp_code
        )  # Assuming this sends the confirmation email

        # Optionally delete OTP record after successful verification
        otp.delete()

        staff_data = serializers.UserSerializer(user).data
        message = "Email verified Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            staff_data,
        )


# *** Staff (Login) *** #
class StaffLoginView(APIView):
    def post(self, request):
        # Deserialize the staff login data
        serializer = serializers.StaffLoginSerializer(data=request.data)

        if serializer.is_valid():
            staff = serializer.validated_data  # Extract the validated staff
            staff_data = serializers.UserSerializer(staff).data

            if not staff.is_verified:
                message = "Your account is not verified. Please verify your account to proceed."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                    staff_data,
                )

            # Generate refresh token and include staff_id in the token payload
            refresh = RefreshToken.for_user(staff)
            refresh["staff_id"] = (
                staff.id
            )  # Explicitly add staff_id to the token payload

            # Generate access token
            access_token = refresh.access_token

            staff_data = serializers.UserSerializer(staff).data
            status_code = status.HTTP_200_OK
            response = {
                "success": "True",
                "code": 0,
                "message": "Staff Login Successfully.",
                "status_code": status_code,
                "data": staff_data,
                "access_token": str(access_token),
                "refresh_token": str(refresh),
            }
            return Response(
                response,
                status=status_code,
            )

        message = serializer.errors
        return utils.FunReturn(
            1,
            message,
            status.HTTP_400_BAD_REQUEST,
        )


# *** Staff (ID) *** #
class StaffIDView(APIView):
    def get(self, request, pk):
        try:
            staff = models.User.objects.get(pk=pk)
        except models.User.DoesNotExist:
            message = "Staff not found."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_404_NOT_FOUND,
            )

        staff_data = serializers.UserSerializer(staff).data

        if staff_data["is_staff"] == False:
            message = "Staff with this Id is not Found."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_404_NOT_FOUND,
            )

        message = "Staff retrieved Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            staff_data,
        )


# *** Staff (Refresh) *** #
class StaffRefreshView(APIView):
    def post(self, request):
        try:
            # Retrieve and decode the refresh token
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                message = {
                    "refresh_token": "This field is required.",
                }
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_404_NOT_FOUND,
                )

            # Decode the JWT token
            payload = jwt.decode(
                refresh_token, SECRET_KEY, algorithms=["HS256"]
            )  # {'token_type': 'refresh', 'exp': 1737402322, 'iat': 1737315922, 'jti': '626f3935d64e4ebcbfcb53d54041f2ab', 'user_id': 1, 'teacher_id': 1}

            # Retrieve user_id from the token payload
            user_id = payload.get("user_id")
            if not user_id:
                raise ValidationError(
                    {
                        "refresh_token": "Invalid token payload.",
                    }
                )

            # Fetch the Staff object
            staff = models.User.objects.get(id=user_id)

            # Serialize the Staff object
            staff_data = serializers.UserSerializer(staff).data
            message = "Staff retrieved Successfully."
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
                staff_data,
            )

        except models.User.DoesNotExist:
            raise ValidationError(
                {
                    "message": "Staff not found.",
                }
            )

        except jwt.ExpiredSignatureError:
            raise ValidationError(
                {
                    "message": "Refresh token has expired.",
                }
            )

        except jwt.InvalidTokenError:
            raise ValidationError(
                {
                    "message": "Invalid refresh token.",
                }
            )

        except Exception as e:
            raise ValidationError(
                {
                    "message": str(e),
                }
            )


# *** Staff (Change Password) *** #
class StaffChangePasswordView(APIView):
    def post(self, request):
        try:
            # Retrieve and decode the refresh token
            refresh_token = request.data.get("refresh_token")

            if not refresh_token:
                raise ValidationError({"refresh_token": "This field is required."})

            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
            staff_id = payload.get("staff_id")

            # Fetch the staff
            staff = models.User.objects.get(id=staff_id)

            # Validate old password
            old_password = request.data.get("old_password")

            if not old_password or not check_password(old_password, staff.password):
                raise ValidationError({"message": "Old password is incorrect."})

            # Validate new passwords
            new_password = request.data.get("new_password")
            confirm_password = request.data.get("confirm_password")

            # validate_password(new_password, confirm_password)

            # Change password
            staff.set_password(new_password)
            staff.save()
            utils.send_change_password_confirm(staff)

            staff_data = serializers.UserSerializer(staff).data
            message = "Password changed Successfully."
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
                staff_data,
            )

        except jwt.ExpiredSignatureError:
            raise ValidationError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValidationError("Invalid token")
        except models.User.DoesNotExist:
            raise ValidationError("Staff not found")
        except ValidationError as e:
            message = e.detail
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )


# *** Staff (Logout) *** #
class StaffLogoutView(APIView):
    def post(self, request):
        try:
            # Get the refresh token from the request
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                message = "Refresh token not provided."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_400_BAD_REQUEST,
                )

            # Decode the refresh token
            token = RefreshToken(refresh_token)
            staff_id_in_token = token.payload.get("user_id")

            if not staff_id_in_token:
                message = "Invalid token: user id missing."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                )

            # Validate that the staff exists and matches the current authenticated staff
            staff = models.User.objects.filter(id=staff_id_in_token).first()
            if not staff:
                message = "Invalid token: staff not found."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                )

            # Expire the token (logout the staff)
            token.set_exp()

            message = "Logout Successful."
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
            )
        except Exception as e:
            message = str(e)
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )


# *** Staff (Reset Password) *** #
class StaffPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            message = "Email is required."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )
        try:
            staff = models.User.objects.get(email=email)
            staff_data = serializers.UserSerializer(staff).data

            if not staff.is_verified:
                message = "Your account is not verified. Please verify your account to proceed."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                    staff_data,
                )

        except models.User.DoesNotExist:
            message = "Admin with this email does not exist."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Send OTP for password reset
        try:
            utils.send_otp_for_password_reset(email, user_type="staff")
            message = "OTP has been sent to your email."
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
            )
        except ValueError as e:
            message = str(e)
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )


# *** Staff (Confirm Reset Password) *** #
class StaffConfirmResetPasswordView(APIView):
    """
    This view allows a staff to reset their password after OTP verification.
    """

    def post(self, request):
        otp = request.data.get("otp")
        password = request.data.get("password")
        password2 = request.data.get("password2")

        if password != password2:
            message = "Passwords do not match."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Validate OTP
        try:
            otp_instance = models.OneTimeOTP.objects.get(otp=otp, user__isnull=False)
        except models.OneTimeOTP.DoesNotExist:
            message = "Invalid OTP."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        if otp_instance.is_expired():
            message = "OTP has expired."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        staff = otp_instance.user
        password = password

        staff.set_password(password)
        staff.save()
        utils.send_reset_password_confirm(staff)

        # Delete the used OTP
        models.OneTimeOTP.objects.filter(user=staff).delete()

        staff_data = serializers.UserSerializer(staff).data
        message = "Confirm Reset Password Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            staff_data,
        )






# ******************************************************************************
# ==============================================================================
# *** 4) Student *** #
# *** Student (Register) *** #
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

# *** Student (Register Verify) *** #
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


# *** Student (Students) *** #
class StudentsListView(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_student=True)

# *** Student (Student ID) -> [GET, POST, PUT, DELETE] *** #
class StudentPKAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_student=True)


# *** Student (Profile) *** #
class StudentProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.StudentProfileSerializer

    def get_queryset(self):
        return models.StudentProfile.objects.all()

    def get_object(self):
        try:
            student_pk = self.kwargs["pk"]  # 1
            student_profile = models.StudentProfile.objects.get(user=student_pk)
            return student_profile
        except models.StudentProfile.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            raise NotFound(
                {
                    "success": "False",
                    "code": 1,
                    "message": "Student Profile not found",
                    "status_code": status_code,
                    "data": "",
                }
            )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        student_data = serializer.data

        if student_data["student"]["is_student"] == False:
            message = "Student Profile whit this id is not Found."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_404_NOT_FOUND,
            )

        message = "Student Profile retrieved Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            student_data,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        student_data = serializer.data
        message = "Student Profile updated Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            student_data,
        )


# *** Student (Resend OTP) *** #
class StudentResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.StudentResendOTPSerializer(data=request.data)

        if not serializer.is_valid():
            message = serializer.errors
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data["email"]
        try:
            user = models.User.objects.get(email=email)

            # Check if the teacher is already verified
            if user.is_verified:
                message = "Your account has already been verified. Please go to the login page."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                )

            # Resend OTP if not verified
            utils.send_otp_for_user(user.email, "student")
        except models.User.DoesNotExist:
            message = "No user found with this email."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_404_NOT_FOUND,
            )

        message = "OTP has been resent to your email."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
        )


# *** Student (Verify Account) *** #
class StudentVerifyAccountView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        otp_code = request.data.get("otp_code")

        # Ensure OTP code is provided
        if not otp_code:
            message = "OTP code is required"
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Retrieve the OTP record from OneTimeOTP model
            otp = models.OneTimeOTP.objects.get(otp=otp_code)
        except models.OneTimeOTP.DoesNotExist:
            message = "Invalid OTP Code"
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Check OTP expiration
        if otp.is_expired():
            message = "OTP has expired"
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Determine if the OTP belongs to a User
        if otp.user:
            user = otp.user
        else:
            message = "No associated user for this OTP code"
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Check if the user is already verified
        if user.is_verified:
            message = "Email already verified"
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
                user,
            )

        # Mark user as verified
        user.is_verified = True
        user.save()

        # Send verification success email
        utils.send_verification_email(
            user, otp_code
        )  # Assuming this sends the confirmation email

        # Optionally delete OTP record after successful verification
        otp.delete()

        teacher_data = serializers.UserSerializer(user).data
        message = "Email verified Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            teacher_data,
        )


# *** Student (Login) *** #
class StudentLoginView(APIView):
    def post(self, request):
        # Deserialize the student login data
        serializer = serializers.StudentLoginSerializer(data=request.data)

        if serializer.is_valid():
            student = serializer.validated_data  # Extract the validated student
            student_data = serializers.UserSerializer(student).data

            if not student.is_verified:
                message = "Your account is not verified. Please verify your account to proceed."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                    student_data,
                )

            # Generate refresh token and include student_id in the token payload
            refresh = RefreshToken.for_user(student)
            refresh["student_id"] = (
                student.id
            )  # Explicitly add student_id to the token payload

            # Generate access token
            access_token = refresh.access_token

            status_code = status.HTTP_200_OK
            response = {
                "success": "True",
                "code": 0,
                "message": "Student Login Successfully.",
                "status_code": status_code,
                "data": student_data,
                "access_token": str(access_token),
                "refresh_token": str(refresh),
            }
            return Response(
                response,
                status=status_code,
            )

        message = serializer.errors
        return utils.FunReturn(
            1,
            message,
            status.HTTP_400_BAD_REQUEST,
        )


# *** Student (ID) *** #
class StudentIDView(APIView):
    def get(self, request, pk):
        try:
            student = models.User.objects.get(pk=pk)
        except models.User.DoesNotExist:
            message = "Student not found."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_404_NOT_FOUND,
            )

        # تحويل الكائن إلى JSON باستخدام Serializer
        student_data = serializers.UserSerializer(student).data

        if student_data["is_student"] == False:
            message = "Student with this Id is not Found."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_404_NOT_FOUND,
            )

        message = "Student retrieved Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            student_data,
        )


# *** Student (Refresh) *** #
class StudentRefreshView(APIView):
    def post(self, request):
        try:
            # Retrieve and decode the refresh token
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                message = (
                    {
                        "refresh_token": "This field is required.",
                    },
                )
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_404_NOT_FOUND,
                )

            # Decode the JWT token
            payload = jwt.decode(
                refresh_token, SECRET_KEY, algorithms=["HS256"]
            )  # {'token_type': 'refresh', 'exp': 1737402322, 'iat': 1737315922, 'jti': '626f3935d64e4ebcbfcb53d54041f2ab', 'user_id': 1, 'teacher_id': 1}

            # Retrieve user_id from the token payload
            user_id = payload.get("user_id")
            if not user_id:
                raise ValidationError(
                    {
                        "refresh_token": "Invalid token payload.",
                    }
                )

            # Fetch the Student object
            student = models.User.objects.get(id=user_id)

            # Serialize the Student object
            student_data = serializers.UserSerializer(student).data
            message = "Student retrieved Successfully."
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
                student_data,
            )

        except models.User.DoesNotExist:
            raise ValidationError(
                {
                    "message": "Student not found.",
                }
            )

        except jwt.ExpiredSignatureError:
            raise ValidationError(
                {
                    "message": "Refresh token has expired.",
                }
            )

        except jwt.InvalidTokenError:
            raise ValidationError(
                {
                    "message": "Invalid refresh token.",
                }
            )

        except Exception as e:
            raise ValidationError(
                {
                    "message": str(e),
                }
            )


# *** Student (Change Password) *** #
class StudentChangePasswordView(APIView):
    def post(self, request):
        try:
            # Retrieve and decode the refresh token
            refresh_token = request.data.get("refresh_token")

            if not refresh_token:
                raise ValidationError({"refresh_token": "This field is required."})

            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
            student_id = payload.get("student_id")

            # Fetch the student
            student = models.User.objects.get(id=student_id)

            # Validate old password
            old_password = request.data.get("old_password")

            if not old_password or not check_password(old_password, student.password):
                raise ValidationError({"message": "Old password is incorrect."})

            # Validate new passwords
            new_password = request.data.get("new_password")
            confirm_password = request.data.get("confirm_password")

            # validate_password(new_password, confirm_password)

            # Change password
            student.set_password(new_password)
            student.save()
            utils.send_change_password_confirm(student)

            student_data = serializers.UserSerializer(student).data
            message = "Password changed successfully."
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
                student_data,
            )
        except jwt.ExpiredSignatureError:
            raise ValidationError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValidationError("Invalid token")
        except models.User.DoesNotExist:
            raise ValidationError("Student not found")
        except ValidationError as e:
            message = e.detail
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )


# *** Student (Logout) *** #
class StudentLogoutView(APIView):
    def post(self, request):
        try:
            # Get the refresh token from the request
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                message = "Refresh token not provided."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_400_BAD_REQUEST,
                )

            # Decode the refresh token
            token = RefreshToken(refresh_token)
            student_id_in_token = token.payload.get("user_id")

            if not student_id_in_token:
                message = "Invalid token: user id missing."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                )

            # Validate that the student exists and matches the current authenticated student
            student = models.User.objects.filter(id=student_id_in_token).first()
            if not student:
                message = "Invalid token: student not found."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                )

            # Expire the token (logout the student)
            token.set_exp()

            message = "Logout Successful."
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
            )
        except Exception as e:
            message = str(e)
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )


# *** Student (Reset Password) *** #
class StudentPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            message = "Email is required."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )
        try:
            student = models.User.objects.get(email=email)
            student_data = serializers.UserSerializer(student).data

            if not student.is_verified:
                message = "Your account is not verified. Please verify your account to proceed."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                    student_data,
                )

        except models.User.DoesNotExist:
            message = "Student with this email does not exist."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Send OTP for password reset
        try:
            utils.send_otp_for_password_reset(email, user_type="student")
            message = "OTP has been sent to your email."
            return utils.FunReturn(
                0,
                message,
                status.HTTP_200_OK,
            )
        except ValueError as e:
            message = str(e)
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )


# *** Student (Confirm Reset Password) *** #
class StudentConfirmResetPasswordView(APIView):
    """
    This view allows a Student to reset their password after OTP verification.
    """

    def post(self, request):
        otp = request.data.get("otp")
        password = request.data.get("password")
        password2 = request.data.get("password2")

        if password != password2:
            message = "Passwords do not match."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        # Validate OTP
        try:
            otp_instance = models.OneTimeOTP.objects.get(otp=otp, user__isnull=False)
        except models.OneTimeOTP.DoesNotExist:
            message = "Invalid OTP."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        if otp_instance.is_expired():
            message = "OTP has expired."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_400_BAD_REQUEST,
            )

        student = otp_instance.user
        password = password

        student.set_password(password)
        student.save()
        utils.send_reset_password_confirm(student)

        # Delete the used OTP
        models.OneTimeOTP.objects.filter(user=student).delete()

        student_data = serializers.UserSerializer(student).data
        message = "Confirm Reset Password Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            student_data,
        )






# ******************************************************************************
# ==============================================================================
# *** 5) Public *** #
# *** User (Users) *** #
class UsersListView(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

# *** User (User ID) -> [GET, POST, PUT, DELETE] *** #
class UserPKAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()


# *** Public (Login) *** #
class PublicLoginView(APIView):
    def post(self, request):
        # Deserialize the user login data
        serializer = serializers.PublicLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data  # Extract the validated user
            user_data = serializers.UserSerializer(user).data

            # Step 2: 
            if not user.is_verified:
                message = "Your account is not verified. Please verify your account to proceed."
                return utils.FunReturn(
                    1,
                    message,
                    status.HTTP_403_FORBIDDEN,
                    user_data,
                )
            
            # Step 3:
            if user_data["is_admin"] == True:
                profile = models.AdminProfile.objects.get(user=user_data["id"])
                user_profile = serializers.AdminProfileSerializer(profile).data
            if user_data["is_teacher"] == True:
                profile = models.TeacherProfile.objects.get(user=user_data["id"])    
                user_profile = serializers.TeacherProfileSerializer(profile).data
            if user_data["is_staff"] == True:
                profile = models.StaffProfile.objects.get(user=user_data["id"])    
                user_profile = serializers.StaffProfileSerializer(profile).data
            if user_data["is_student"] == True:
                profile = models.StudentProfile.objects.get(user=user_data["id"])    
                user_profile = serializers.StudentProfileSerializer(profile).data

            # Generate refresh token and include user_id in the token payload
            refresh = RefreshToken.for_user(user)
            refresh["user_id"] = (
                user.id
            )  # Explicitly add user_id to the token payload
            # Generate access token
            access_token = refresh.access_token

            status_code = status.HTTP_200_OK
            response = {
                "success": "True",
                "code": 0,
                "message": "User Login Successfully.",
                "status_code": status_code,
                "data": user_data,
                "profile": user_profile,
                "access_token": str(access_token),
                "refresh_token": str(refresh),
            }
            return Response(
                response,
                status=status_code,
            )

        message = serializer.errors
        return utils.FunReturn(
            1,
            message,
            status.HTTP_400_BAD_REQUEST,
        )


# *** Public (ID) *** #
class PublicIDView(APIView):
    def get(self, request, pk):
        # Step 1:
        try:
            user = models.User.objects.get(pk=pk)
        except models.User.DoesNotExist:
            message = "User not found."
            return utils.FunReturn(
                1,
                message,
                status.HTTP_404_NOT_FOUND,
            )

        # Step 2:
        # تحويل الكائن إلى JSON باستخدام Serializer
        user_data = serializers.UserSerializer(user).data

        # Step 3:
        message = "User Retrieved Successfully."
        return utils.FunReturn(
            0,
            message,
            status.HTTP_200_OK,
            user_data,
        )




# *****************************************************************
# =================================================================