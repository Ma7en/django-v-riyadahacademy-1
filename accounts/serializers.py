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
from accounts import models
from accounts import utils


# *****************************************************************
# =================================================================
# *** User *** #
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }


# *****************************************************************
# =================================================================
# *** One Time OTP *** #
class OneTimeOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OneTimeOTP
        fields = "__all__"


# *****************************************************************
# =================================================================
# *** Admin (Profile) *** #
class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdminProfile
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        # print(
        #     "response", response
        # )  # response {'id': 1, 'gender': None, 'image': 'http://127.0.0.1:8000/media/user/default-user.png', 'phone_number': None, 'age': None, 'created_at': '2025-01-22T14:08:28.986408Z', 'user': 1}
        response["admin"] = UserSerializer(instance.user).data
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


# *****************************************************************
# =================================================================
# *** Teacher (Profile) *** #
class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TeacherProfile
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["teacher"] = UserSerializer(instance.user).data
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


# *****************************************************************
# =================================================================
# *** Staff Profile *** #
class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StaffProfile
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["staff"] = UserSerializer(instance.user).data
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


# *****************************************************************
# =================================================================
# *** Student Profile *** #
class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentProfile
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["student"] = UserSerializer(instance.user).data
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


# *****************************************************************
# =================================================================
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
            raise AuthenticationFailed(_("Invalid Email or Password."))

        # Authenticate user by verifying the password
        if not user.check_password(password):
            raise AuthenticationFailed(_("Invalid Email or Password."))

        # Check if the user is active
        if not user.is_active:
            raise AuthenticationFailed(_("user account is deactivated."))

        return user



# *****************************************************************
# =================================================================

