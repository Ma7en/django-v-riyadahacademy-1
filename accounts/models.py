#
import uuid



#
from datetime import timedelta



#
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver



#
from .managers import UserManager





# ******************************************************************************
# ==============================================================================
# *** User *** #
class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(
        # verbose_name="email address",
        max_length=1_000,
        unique=True,
    )
    first_name = models.CharField(max_length=1_000)
    last_name = models.CharField(max_length=1_000)

    username = models.CharField(
        max_length=1_000,
        null=True,
        blank=True,
    )
    full_name = models.CharField(
        max_length=1_000,
        null=True,
        blank=True,
    )

    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return f"{self.id}): ({self.email})"

    def save(self, *args, **kwargs):
        email_username, _ = self.email.split("@")
        if self.first_name and self.last_name:
            self.full_name = self.first_name + " " + self.last_name
        if self.full_name == "" or self.full_name == None:
            self.full_name = email_username
        if self.username == "" or self.username == None:
            self.username = email_username

        super(User, self).save(*args, **kwargs)





# ******************************************************************************
# ==============================================================================
# *** Superuser Profile  *** #
class SuperuserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="superuser_profile",
        unique=False,
    )

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    gender = models.CharField(
        max_length=30,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )

    POWERS_CHOICES = (
        ("Complete", "كاملة"),
        ("Medium", "متوسطة"),
        ("Limited", "محدودة"),
    )
    powers = models.CharField(
        max_length=30,
        choices=POWERS_CHOICES,
        default="Complete",
        null=True,
        blank=True,
    )

    image = models.ImageField(
        upload_to="user/superuser",
        default="user/default-user.png",
        null=True,
        blank=True,
    )

    bio = models.TextField(
        max_length=10_00, 
        null=True, 
        blank=True,
    )

    # phone_number = models.CharField(
    #     max_length=11,
    #     validators=[
    #         RegexValidator(
    #             regex="^01[0|1|2|5][0-9]{8}$",
    #             message="Phone must be start 010, 011, 012, 015 and all number contains 11 digits",
    #         )
    #     ],
    #     null=True,
    #     blank=True,
    # )
    phone_number = models.CharField(
        max_length=10,  # الأرقام السعودية تتكون من 10 أرقام (بدون +966)
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^(05)(5|0|3|6|4|9|1|8|7|2)([0-9]{7})$',
                message='يجب أن يبدأ رقم الهاتف بـ 05 ويحتوي على 10 أرقام صحيحة'
            )
        ],
        # verbose_name="رقم الجوال السعودي",
        null=True, 
        blank=True,
    )
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.id}): ({self.user.email})"


# ******************************************************************************
# ==============================================================================
# *** Admin Profile  *** #
class AdminProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="admin_profile",
        unique=False,
    )

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    gender = models.CharField(
        max_length=30,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )

    POWERS_CHOICES = (
        ("Complete", "كاملة"),
        ("Medium", "متوسطة"),
        ("Limited", "محدودة"),
    )
    powers = models.CharField(
        max_length=30,
        choices=POWERS_CHOICES,
        default="Complete",
        null=True,
        blank=True,
    )

    image = models.ImageField(
        upload_to="user/admin",
        default="user/default-user.png",
        null=True,
        blank=True,
    )

    bio = models.TextField(
        max_length=10_00, 
        null=True, 
        blank=True,
    )

    # phone_number = models.CharField(
    #     max_length=11,
    #     validators=[
    #         RegexValidator(
    #             regex="^01[0|1|2|5][0-9]{8}$",
    #             message="Phone must be start 010, 011, 012, 015 and all number contains 11 digits",
    #         )
    #     ],
    #     null=True,
    #     blank=True,
    # )
    phone_number = models.CharField(
        max_length=10,  # الأرقام السعودية تتكون من 10 أرقام (بدون +966)
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^(05)(5|0|3|6|4|9|1|8|7|2)([0-9]{7})$',
                message='يجب أن يبدأ رقم الهاتف بـ 05 ويحتوي على 10 أرقام صحيحة'
            )
        ],
        # verbose_name="رقم الجوال السعودي",
        null=True, 
        blank=True,
    )
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    # class Meta:
    #     """
    #     to set table name in database
    #     """
    #     db_table = "admin_profile"

    def __str__(self):
        return f"{self.id}): ({self.user.email})"





# ******************************************************************************
# ==============================================================================
# *** Teacher Profile *** #
class TeacherProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
        unique=False,
    )

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    gender = models.CharField(
        max_length=30,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )

    image = models.ImageField(
        upload_to="user/teacher",
        default="user/default-user.png",
        null=True,
        blank=True,
    )
    # phone_number = models.CharField(
    #     max_length=11,
    #     validators=[
    #         RegexValidator(
    #             regex="^01[0|1|2|5][0-9]{8}$",
    #             message="Phone must be start 010, 011, 012, 015 and all number contains 11 digits",
    #         )
    #     ],
    #     null=True,
    #     blank=True,
    # )
    
    bio = models.TextField(
        max_length=10_00, 
        null=True, 
        blank=True,
    )

    phone_number = models.CharField(
        max_length=10,  # الأرقام السعودية تتكون من 10 أرقام (بدون +966)
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^(05)(5|0|3|6|4|9|1|8|7|2)([0-9]{7})$',
                message='يجب أن يبدأ رقم الهاتف بـ 05 ويحتوي على 10 أرقام صحيحة'
            )
        ],
        # verbose_name="رقم الجوال السعودي",
        null=True, 
        blank=True,
    )
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    # class Meta:
    #     """
    #     to set table name in database
    #     """
    #     db_table = "teacher_profile"

    def __str__(self):
        return f"{self.id}): ({self.user.email})"





# ******************************************************************************
# ==============================================================================
# *** Staff Profile *** #
class StaffProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="staff_profile",
        unique=False,
    )

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    gender = models.CharField(
        max_length=30,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )

    image = models.ImageField(
        upload_to="user/staff",
        default="user/default-user.png",
        null=True,
        blank=True,
    )
    
    bio = models.TextField(
        max_length=10_00, 
        null=True, 
        blank=True,
    )

    # phone_number = models.CharField(
    #     max_length=11,
    #     validators=[
    #         RegexValidator(
    #             regex="^01[0|1|2|5][0-9]{8}$",
    #             message="Phone must be start 010, 011, 012, 015 and all number contains 11 digits",
    #         )
    #     ],
    #     null=True,
    #     blank=True,
    # )
    phone_number = models.CharField(
        max_length=10,  # الأرقام السعودية تتكون من 10 أرقام (بدون +966)
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^(05)(5|0|3|6|4|9|1|8|7|2)([0-9]{7})$',
                message='يجب أن يبدأ رقم الهاتف بـ 05 ويحتوي على 10 أرقام صحيحة'
            )
        ],
        # verbose_name="رقم الجوال السعودي",
        null=True, 
        blank=True,
    )
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    # class Meta:
    #     """
    #     to set table name in database
    #     """
    #     db_table = "staff_profile"

    def __str__(self):
        return f"{self.id}): ({self.phone_number})"





# ******************************************************************************
# ==============================================================================
# *** Student Profile *** #
class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile",
        unique=False,
    )

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    gender = models.CharField(
        max_length=30,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )

    image = models.ImageField(
        upload_to="user/student",
        default="user/default-user.png",
        null=True,
        blank=True,
    )
    
    bio = models.TextField(
        max_length=10_00, 
        null=True, 
        blank=True,
    )

    # phone_number = models.CharField(
    #     max_length=11,
    #     validators=[
    #         RegexValidator(
    #             regex="^01[0|1|2|5][0-9]{8}$",
    #             message="Phone must be start 010, 011, 012, 015 and all number contains 11 digits",
    #         )
    #     ],
    #     null=True,
    #     blank=True,
    # )
    phone_number = models.CharField(
        max_length=10,  # الأرقام السعودية تتكون من 10 أرقام (بدون +966)
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^(05)(5|0|3|6|4|9|1|8|7|2)([0-9]{7})$',
                message='يجب أن يبدأ رقم الهاتف بـ 05 ويحتوي على 10 أرقام صحيحة'
            )
        ],
        # verbose_name="رقم الجوال السعودي",
        null=True, 
        blank=True,
    )

    age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    # class Meta:
    #     """
    #     to set table name in database
    #     """
    #     db_table = "student_profile"

    def __str__(self):
        return f"{self.id}): ({self.phone_number})"





# ******************************************************************************
# ==============================================================================
# *** (One Time OTP) *** #
class OneTimeOTP(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    otp = models.CharField(max_length=6)
    token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        # unique=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def is_expired(self):
        expiry_time = self.created_at + timedelta(minutes=10)
        return timezone.now() > expiry_time

    def __str__(self):
        if self.user:
            return f"{self.id}): ({self.user.email}) - OTP code"
        return f"{self.id}): {self.otp} OTP Code"





# ******************************************************************************
# ==============================================================================
# ***  *** #



