#
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse



#
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError


# 



#
from . import models
from . import utils





# ******************************************************************************
# ==============================================================================
# *** User *** #
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"
        # fields = [        
        # "id",
        # "last_login",
        # "date_joined",
        # "email",
        # "first_name",
        # "last_name",
        # "username",
        # "full_name",
        # "is_superuser",
        # "is_admin",
        # "is_teacher",
        # "is_staff",
        # "is_student",
        # "is_active",
        # "is_verified",
        # ]
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
            "groups": {
                "write_only": True,
            },
            "user_permissions": {
                "write_only": True,
                
            }
        }



# ******************************************************************************
# ==============================================================================
# *** One Time OTP *** #
class OneTimeOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OneTimeOTP
        # fields = "__all__"
        fields = [
            "id",
            "user",
            
            "otp",
            "token",
            
            "created_at",

            "is_expired",
        ]



# ******************************************************************************
# ============================================================================== 
# *** Superuser (Profile) *** #
class SuperuserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all()) 

    class Meta:
        model = models.SuperuserProfile
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["superuser"] = UserSerializer(instance.user).data
        return response


# ******************************************************************************
# ============================================================================== 
# *** Admin (Profile) *** #
class AdminProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all()) 

    class Meta:
        model = models.AdminProfile
        fields = "__all__"
        # fields = [
        #     "id",

        #     "user",

        #     "gender",
        #     "powers",
        #     "image",

        # ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # print(
        #     "response", response
        # )  # response {'id': 1, 'gender': None, 'image': 'http://127.0.0.1:8000/media/user/default-user.png', 'phone_number': None, 'age': None, 'created_at': '2025-01-22T14:08:28.986408Z', 'user': 1}
        response["user"] = UserSerializer(instance.user).data
        return response


# *** Admin (Register) *** #
class AdminRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

    def validate(self, attrs):
        # Define a validation method to check if the passwords match
        if attrs["password"] != attrs["password2"]:
            # Raise a validation error if the passwords don't match
            raise serializers.ValidationError(
                {
                    "password": "Password fields didn't match.",
                }
            )
        # Return the validated attributes
        return attrs

    def create(self, validated_data):
        user = models.User.objects.create_adminuser(**validated_data)
        return user


# *** Admin (Resend OTP) *** #
class AdminResendOTPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = models.User
        fields = ["email"]

    def validate_email(self, value):
        """
        Ensure the email exists in the User model.
        """
        if not models.User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("No admin found with this email."))
        return value


# *** Admin (Verify Account) *** #
class AdminVerifyAccountSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)



# *** Admin (Login) *** #
class AdminLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=500)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            # Fetch the Admin by email
            admin = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            raise AuthenticationFailed(_("Invalid Email or Password.."))

        # Authenticate admin by verifying the password
        if not admin.check_password(password):
            raise AuthenticationFailed(_("Invalid Email or Password.."))

        # Check if the admin is active
        if not admin.is_active:
            raise AuthenticationFailed(_("admin account is deactivated..."))

        return admin



# *** Admin (Refresh) *** #
class AdminRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=10_000)



# *** Admin (Change Password) *** #
class AdminChangePasswordSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=10_000)
    old_password = serializers.CharField(max_length=10_000)
    new_password = serializers.CharField(max_length=10_000)
    confirm_password = serializers.CharField(max_length=10_000)



# *** Admin (Logout) *** #
class AdminLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=10_000)





# *** Admin (Password Reset) *** #
class AdminPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=10_000)




# *** Admin (Confirm Reset Password) *** #
class AdminConfirmResetPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=10_000)
    password = serializers.CharField(max_length=10_000)
    password2 = serializers.CharField(max_length=10_000)

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data









# ******************************************************************************
# ==============================================================================
# *** Teacher (Profile) *** #
class TeacherProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all()) 

    class Meta:
        model = models.TeacherProfile
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["user"] = UserSerializer(instance.user).data
        return response


# *** Teacher (Register) *** #
class TeacherRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
            # "profile",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

    def validate(self, attrs):
        # Define a validation method to check if the passwords match
        if attrs["password"] != attrs["password2"]:
            # Raise a validation error if the passwords don't match
            raise serializers.ValidationError(
                {
                    "password": "Password fields didn't match.",
                }
            )
        # Return the validated attributes
        return attrs

    def create(self, validated_data):
        user = models.User.objects.create_teacheruser(**validated_data)
        return user


# *** Teacher (Resend OTP) *** #
class TeacherResendOTPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = models.User
        fields = ["email"]

    def validate_email(self, value):
        """
        Ensure the email exists in the User model.
        """
        if not models.User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("No teacher found with this email."))
        return value


# *** Teacher (Verify Account) *** #
class TeacherVerifyAccountSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)


# *** Teacher (Login) *** #
class TeacherLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=500)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            # Fetch the Teacher by email
            teacher = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            raise AuthenticationFailed(_("Invalid Email or Password."))

        # Authenticate teacher by verifying the password
        if not teacher.check_password(password):
            raise AuthenticationFailed(_("Invalid Email or Password."))

        # Check if the teacher is active
        if not teacher.is_active:
            raise AuthenticationFailed(_("teacher account is deactivated."))

        return teacher


# *** Teacher (Refresh) *** #
class TeacherRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=10_000)


# *** Teacher (Change Password) *** #
class TeacherChangePasswordSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=10_000)
    old_password = serializers.CharField(max_length=10_000)
    new_password = serializers.CharField(max_length=10_000)
    confirm_password = serializers.CharField(max_length=10_000)



# *** Teacher (Logout) *** #
class TeacherLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=10_000)



# *** Teacher (Password Reset) *** #
class TeacherPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=10_000)



# *** Teacher (Confirm Reset Password) *** #
class TeacherConfirmResetPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=10_000)
    password = serializers.CharField(max_length=10_000)
    password2 = serializers.CharField(max_length=10_000)

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data











# ******************************************************************************
# ==============================================================================
# *** Staff Profile *** #
class StaffProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all()) 

    class Meta:
        model = models.StaffProfile
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["user"] = UserSerializer(instance.user).data
        return response


# *** Staff Register *** #
class StaffRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

    def validate(self, attrs):
        # Define a validation method to check if the passwords match
        if attrs["password"] != attrs["password2"]:
            # Raise a validation error if the passwords don't match
            raise serializers.ValidationError(
                {
                    "password": "Password fields didn't match.",
                }
            )
        # Return the validated attributes
        return attrs

    def create(self, validated_data):
        user = models.User.objects.create_staffuser(**validated_data)
        return user


# *** Staff (Resend OTP) *** #
class StaffResendOTPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = models.User
        fields = ["email"]

    def validate_email(self, value):
        """
        Ensure the email exists in the User model.
        """
        if not models.User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("No teacher found with this email."))
        return value


# *** Staff (Verify Account) *** #
class StaffVerifyAccountSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)


# *** Staff (Login) *** #
class StaffLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=500)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            # Fetch the staff by email
            staff = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            raise AuthenticationFailed(_("Invalid Email or Password."))

        # Authenticate staff by verifying the password
        if not staff.check_password(password):
            raise AuthenticationFailed(_("Invalid Email or Password."))

        # Check if the staff is active
        if not staff.is_active:
            raise AuthenticationFailed(_("staff account is deactivated."))

        return staff


# *** Staff (Refresh) *** #
class StaffRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=10_000)


# *** Staff (Change Password) *** #
class StaffChangePasswordSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=10_000)
    old_password = serializers.CharField(max_length=10_000)
    new_password = serializers.CharField(max_length=10_000)
    confirm_password = serializers.CharField(max_length=10_000)




# *** Staff (Logout) *** #
class StaffLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=10_000)




# *** Staff (Password Reset) *** #
class StaffPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=10_000)




# *** Staff (Confirm Reset Password) *** #
class StaffConfirmResetPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=10_000)
    password = serializers.CharField(max_length=10_000)
    password2 = serializers.CharField(max_length=10_000)

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data










# ******************************************************************************
# ==============================================================================
# *** Student Profile *** #
class StudentProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all()) 

    class Meta:
        model = models.StudentProfile
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["user"] = UserSerializer(instance.user).data
        return response


# *** Student Register *** #
class StudentRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

    def validate(self, attrs):
        # Define a validation method to check if the passwords match
        if attrs["password"] != attrs["password2"]:
            # Raise a validation error if the passwords don't match
            raise serializers.ValidationError(
                {
                    "password": "Password fields didn't match.",
                }
            )
        # Return the validated attributes
        return attrs

    def create(self, validated_data):
        user = models.User.objects.create_studentuser(**validated_data)
        return user


# *** Student (Resend OTP) *** #
class StudentResendOTPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = models.User
        fields = ["email"]

    def validate_email(self, value):
        """
        Ensure the email exists in the User model.
        """
        if not models.User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("No student found with this email."))
        return value



# *** Student (Verify Account) *** #
class StudentVerifyAccountSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)



# *** Student (Login) *** #
class StudentLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=500)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            # Fetch the student by email
            student = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            raise AuthenticationFailed(_("Invalid Email or Password."))

        # Authenticate student by verifying the password
        if not student.check_password(password):
            raise AuthenticationFailed(_("Invalid Email or Password."))

        # Check if the student is active
        if not student.is_active:
            raise AuthenticationFailed(_("student account is deactivated."))

        return student



# *** Student (Refresh) *** #
class StudentRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=10_000)



# *** Student (Change Password) *** #
class StudentChangePasswordSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=10_000)
    old_password = serializers.CharField(max_length=10_000)
    new_password = serializers.CharField(max_length=10_000)
    confirm_password = serializers.CharField(max_length=10_000)


# *** Student (Logout) *** #
class StudentLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=10_000)



# *** Student (Password Reset) *** #
class StudentPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=10_000)



# *** Student (Confirm Reset Password) *** #
class StudentConfirmResetPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=10_000)
    password = serializers.CharField(max_length=10_000)
    password2 = serializers.CharField(max_length=10_000)

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data














# ******************************************************************************
# ==============================================================================
# *** 5) Public *** #
class PublicLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=500)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            # Fetch the user by email
            user = models.User.objects.get(email=email)
        except models.User.DoesNotExist:
            raise AuthenticationFailed(_("No user found with this email."))

        # Authenticate user by verifying the password
        if not user.check_password(password):
            raise AuthenticationFailed(_("Invalid Password."))

        # Check if the user is active
        # if not user.is_active:
        #     raise AuthenticationFailed(_("user account is deactivated."))

        return user


# *** Public (Verify Account) *** #
class PublicVerifyAccountSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)


# *** Public (Resend OTP) *** #
class PublicResendOTPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)


# *** Public (Refresh) *** #
class PublicRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=10_000)

    class Meta:
        model = models.User
        fields = ["email"]

    def validate_email(self, value):
        """
        Ensure the email exists in the User model.
        """
        if not models.User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("No user found with this email."))
        return value




# *** Public (Change Password) *** #
class PublicChangePasswordSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=10_000)
    old_password = serializers.CharField(max_length=10_000)
    new_password = serializers.CharField(max_length=10_000)
    confirm_password = serializers.CharField(max_length=10_000)


# *** Public (Logout) *** #
class PublicLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=10_000)



# *** Public (Password Reset) *** #
class PublicPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=10_000)



# *** Public (Confirm Reset Password) *** #
class PublicConfirmResetPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=10_000)
    password = serializers.CharField(max_length=10_000)
    password2 = serializers.CharField(max_length=10_000)

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data



# *****************************************************************
# =================================================================

