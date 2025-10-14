#
import uuid



#
from datetime import timedelta



#
from django.utils import timezone
from django.dispatch import receiver

from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from django.core.validators import RegexValidator
from django.core.files.storage import default_storage



#
from .managers import UserManager





# ******************************************************************************
# ==============================================================================
# *** User *** #
class User(AbstractUser, PermissionsMixin):
    # logged_in_user_session_key = models.CharField(max_length=255, blank=True, null=True)
    # jwt_token_key = models.UUIDField(default=uuid.uuid4)

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

    # @property
    # def profile(self):
    #     if hasattr(self, 'superuser_profile'):
    #         return self.superuser_profile
    #     elif hasattr(self, 'admin_profile'):
    #         return self.admin_profile
    #     elif hasattr(self, 'teacher_profile'):
    #         return self.teacher_profile
    #     elif hasattr(self, 'staff_profile'):
    #         return self.staff_profile
    #     elif hasattr(self, 'student_profile'):
    #         return self.student_profile
    #     return None

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
        max_length=1_000,
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
        max_length=1_000,
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
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural="1-1) Superuser Profile"

    def __str__(self):
        return f"{self.id}): ({self.user.email})"
    

    def save(self, *args, **kwargs):
        if self.pk:

            # image
            old_instance_image = SuperuserProfile.objects.get(pk=self.pk)
            if old_instance_image.image and old_instance_image.image != self.image:
                default_storage.delete(old_instance_image.image.path)
                self.updated_at = timezone.now()

        super(SuperuserProfile, self).save(*args, **kwargs)



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
        max_length=1_000,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )

    POWERS_CHOICES = (
        ("complete", "كاملة"),
        ("medium", "متوسطة"),
        ("limited", "محدودة"),
    )
    powers = models.CharField(
        max_length=1_000,
        choices=POWERS_CHOICES,
        default="complete",
        null=True,
        blank=True,
    )

    WORK_CHOICES = (
        ("system_manager", "مدير النظام"),
        ("technical_manager", "مدير التقنية"),
        ("programming_manager", "مدير قسم البرمجة"),
        ("content_manager", "مدير المحتوى"),
        ("sales_manager", "مدير المبيعات"),
        ("resources_manager", "مدير الموارد"),
        ("projects_manager", "مدير المشاريع"),
        ("academic_affairs_manager", "مدير الشؤون الأكاديمية"),
        ("supervisor", "مشرف"),
        ("users_supervisor", "مشرف المستخدمين"),
        ("courses_supervisor", "مشرف الدورات"),
        ("marketing_supervisor", "مشرف التسويق"),
        ("support_supervisor", "مشرف الدعم"),
        ("financial_supervisor", "مشرف المالية"),
        ("quality_supervisor", "مشرف الجودة"),
        ("public_relations_supervisor", "مشرف العلاقات العامة"),
        ("recruitment_supervisor", "مشرف التوظيف"),
        ("customer_service_supervisor", "مشرف خدمة العملاء"),
        ("training_supervisor", "مشرف التدريب"),
    )
    work = models.CharField(
        max_length=1_000,
        choices=WORK_CHOICES,
        default="system_manager",
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
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     """
    #     to set table name in database
    #     """
    #     db_table = "admin_profile"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural="1-2) Admin Profile"

    def __str__(self):
        return f"{self.id}): ({self.user.email})"

    def save(self, *args, **kwargs):
        if self.pk:

            # image
            old_instance = AdminProfile.objects.get(pk=self.pk)
            if old_instance.image and old_instance.image != self.image:
                default_storage.delete(old_instance.image.path)
                self.updated_at = timezone.now()

        super(AdminProfile, self).save(*args, **kwargs)




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
        max_length=1_000,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )

    SUBJECT_CHOICES = (
        ("mathematics", "رياضيات"),
        ("advanced_mathematics", "رياضيات متقدمة"),
        ("applied_mathematics", "رياضيات تطبيقية"),
        ("chemistry", "كيمياء"),
        ("organic_chemistry", "كيمياء عضوية"),
        ("physics", "فيزياء"),
        ("advanced_physics", "فيزياء متقدمة"),
        ("biology", "أحياء"),
        ("molecular_biology", "أحياء جزيئية"),
        ("computer_science", "علوم الحاسب"),
        ("advanced_computer_science", "علوم حاسب متقدمة"),
        ("information_technology", "تقنية معلومات"),
        ("arabic_language", "لغة عربية"),
        ("english_language", "لغة إنجليزية"),
        ("advanced_english_language", "لغة انجليزية متقدمة"),
        ("history", "تاريخ"),
        ("geography", "جغرافيا"),
        ("psychology", "علم النفس"),
        ("environmental_science", "علوم بيئية"),
    )
    subject = models.CharField(
        max_length=1_000,
        choices=SUBJECT_CHOICES,
        default="mathematics",
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
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     """
    #     to set table name in database
    #     """
    #     db_table = "teacher_profile"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural="1-3) Teacher Profile"

    def __str__(self):
        return f"{self.id}): ({self.user.email})"

    def save(self, *args, **kwargs):
        if self.pk:
            
            # image
            old_instance_image = TeacherProfile.objects.get(pk=self.pk)
            if old_instance_image.image and old_instance_image.image != self.image:
                default_storage.delete(old_instance_image.image.path)
                self.updated_at = timezone.now()

        super(TeacherProfile, self).save(*args, **kwargs)




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
        max_length=1_000,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )

    POSITION_CHOICES = (
        ("finance", "المالية"),
        ("hr_manager", "مدير الموارد البشرية"),
        ("accounting", "محاسبة"),
        ("it_manager", "مدير تقنية المعلومات"),
        ("customer_service_supervisor", "مشرفة خدمة العملاء"),
        ("facilities_manager", "مدير المرافق"),
        ("administrative_assistant", "مساعدة إدارية"),
        ("security_supervisor", "مشرف الأمن"),
        ("public_relations_coordinator", "منسقة علاقات عامة"),
        ("procurement_manager", "مدير المشتريات"),
        ("recruitment_specialist", "أخصائية توظيف"),
        ("maintenance_supervisor", "مشرف صيانة"),
        ("librarian", "أمينة مكتبة"),
        ("transportation_supervisor", "مشرف النقل"),
        ("marketing_specialist", "أخصائية تسويق"),
        ("quality_manager", "مدير الجودة"),
    )
    position = models.CharField(
        max_length=1_000,
        choices=POSITION_CHOICES,
        default="finance",
        null=True,
        blank=True,
    )

    DEPARTMENT_CHOICES = (
        ("employee_affairs", "شؤون الموظفين"),
        ("finance", "المالية"),
        ("information_technology", "تقنية المعلومات"),
        ("customer_service", "خدمة العملاء"),
        ("facilities", "المرافق"),
        ("student_affairs", "شؤون الطلاب"),
        ("security", "الأمن"),
        ("public_relations", "العلاقات العامة"),
        ("procurement", "المشتريات"),
        ("human_resources", "الموارد البشرية"),
        ("maintenance", "الصيانة"),
        ("library", "المكتبة"),
        ("transportation", "النقل"),
        ("marketing", "التسويق"),
        ("quality", "الجودة"),
    )
    department = models.CharField(
        max_length=1_000,
        choices=DEPARTMENT_CHOICES,
        default="employee_affairs",
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
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     """
    #     to set table name in database
    #     """
    #     db_table = "staff_profile"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural="1-4) Staff Profile"

    def __str__(self):
        return f"{self.id}): ({self.phone_number})"

    def save(self, *args, **kwargs):
        if self.pk:

            # image
            old_instance_image = StaffProfile.objects.get(pk=self.pk)
            if old_instance_image.image and old_instance_image.image != self.image:
                default_storage.delete(old_instance_image.image.path)
                self.updated_at = timezone.now()

        super(StaffProfile, self).save(*args, **kwargs)




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
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     """
    #     to set table name in database
    #     """
    #     db_table = "student_profile"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural="1-5) Student Profile"

    def __str__(self):
        return f"{self.id}): ({self.phone_number})"

    def save(self, *args, **kwargs):
        if self.pk:

            # image
            old_instance_image = StudentProfile.objects.get(pk=self.pk)
            if old_instance_image.image and old_instance_image.image != self.image:
                default_storage.delete(old_instance_image.image.path)
                self.updated_at = timezone.now()

        super(StudentProfile, self).save(*args, **kwargs)




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



