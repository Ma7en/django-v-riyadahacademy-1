#
import shortuuid
import json



#
from django.db import models
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.files.storage import default_storage



# 
from accounts.models import *



# Create your models here.





# ******************************************************************************
# ==============================================================================
# ***  startapp  *** #
class Startapp(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,        
        related_name='startapp_user',
        null=True,
        blank=True,
    )

    CONTENT_TYPE_CHOICES = (
        ("text", "نص"),
        ("image", "صورة"),
        ("link", "رابط"),
        ("file", "ملف"),
    )
    content_type = models.CharField(
        max_length=1_000, 
        choices=CONTENT_TYPE_CHOICES,
        default="text",
        null=True,
        blank=True,
    )

    description = models.TextField(
        max_length=100_000, 
        null=True, 
        blank=True,
    )
    
    image = models.ImageField(
        upload_to="startapp/images", 
        null=True,
        blank=True,
    )
    image_url = models.URLField(null=True, blank=True)

    file = models.FileField(upload_to="startapp/files", null=True, blank=True)

    link_url = models.URLField(null=True, blank=True)

    is_visible = models.BooleanField(default=True)

    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}):  - ({self.is_visible})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "9-1] startapp"

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.is_visible) + "-" + shortuuid.uuid()[:2]
        
        
        if self.pk:

            # image
            old_instance_image = Startapp.objects.get(pk=self.pk)
            if old_instance_image.image and old_instance_image.image != self.image:
                default_storage.delete(old_instance_image.image.path)

        super(Startapp, self).save(*args, **kwargs)






# ******************************************************************************
# ==============================================================================
# *** Category Section *** #
class CategorySection(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='category_section',
    )

    title = models.CharField(max_length=1_000)
    description = models.TextField(
        max_length=10_000, 
        null=True, 
        blank=True,
    )
    
    image = models.ImageField(
        upload_to="categorysection", 
        null=True,
        blank=True,
    )
    image_url = models.URLField(null=True, blank=True)
    
    is_visible = models.BooleanField(default=True)

    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)


    def total_section_course(self):
        return SectionCourse.objects.filter(category=self).count()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural="1-1. Categories Sections"

    def __str__(self) :
        return f"{self.id}): ({self.title}) - [{self.user}] - ({self.is_visible})"
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title) + "-" + shortuuid.uuid()[:2]

        if self.pk:

            # image
            old_instance_image = CategorySection.objects.get(pk=self.pk)
            if old_instance_image.image and old_instance_image.image != self.image:
                default_storage.delete(old_instance_image.image.path)

        super(CategorySection, self).save(*args, **kwargs)
    



# ******************************************************************************
# ==============================================================================
# *** Section Course *** #
class SectionCourse(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='section_course',
    )
    category = models.ForeignKey(
        CategorySection, 
        on_delete=models.CASCADE, 
        related_name='category_section_course',
    )

    title = models.CharField(max_length=1_000)
    description = models.TextField(
        max_length=10_000, 
        null=True, 
        blank=True,
    )
    grade = models.CharField(
        max_length=1_000,
        null=True, 
        blank=True,
    )
    
    image = models.ImageField(
        upload_to="sectioncourse", 
        null=True,
        blank=True,
    )
    image_url = models.URLField(null=True, blank=True)

    is_visible = models.BooleanField(default=True)

    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_course(self):
        return Course.objects.filter(section=self).count()

    def total_question_bank(self):
        return QuestionBank.objects.filter(section=self).count()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural="1-2. Section Course"

    def __str__(self):
        return f"{self.id}): ({self.title}) - [{self.user}] - ({self.is_visible})"
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title) + "-" + shortuuid.uuid()[:2]

        if self.pk:
            old_instance = SectionCourse.objects.get(pk=self.pk)
            if old_instance.image and old_instance.image != self.image:
                default_storage.delete(old_instance.image.path)

        super(SectionCourse, self).save(*args, **kwargs)




# ******************************************************************************
# ==============================================================================
# *** Course *** #
class Course(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses',
    )
    # admin_profile = models.ForeignKey(
    #     AdminProfile,
    #     on_delete=models.CASCADE,
    #     related_name="admin_profile_course",
    #     null=True,
    #     blank=True,
    # )
    # teacher_profile = models.ForeignKey(
    #     TeacherProfile,
    #     on_delete=models.CASCADE,
    #     related_name="teacher_profile_course",
    #     null=True,
    #     blank=True,
    # )
    section = models.ForeignKey(
        SectionCourse, 
        on_delete=models.CASCADE, 
        related_name='section_course',
    )

    STATUS_CHOICES = (
        ("in_progress", "جاري العمل"),
        ("updated", "يتم التحديث"),
        ("complete", "مكتمل"), 
    )
    status = models.CharField(
        max_length=1_000, 
        choices=STATUS_CHOICES, 
        default="in_progress",
        null=True,
        blank=True,
    )
    
    LEVEL_CHOICES = [
        ('beginner', 'مبتدئ'),
        ('intermediate', 'متوسط'),
        ('advanced', 'متقدم'),
    ]
    level = models.CharField(
        max_length=1_000,
        choices=LEVEL_CHOICES, # edithere
        default="beginner",
        null=True, 
        blank=True,
    )

    title = models.CharField(max_length=1_000)
    description = models.TextField(max_length=10_000, null=True, blank=True)
    image = models.ImageField(upload_to="course/images", null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    reviews_count = models.PositiveIntegerField(default=0)
    students_count = models.PositiveIntegerField(default=0)
    
    # 
    # lesson_count = models.PositiveIntegerField(default=0)
    # students_count = models.PositiveIntegerField(default=0)

    # 
    # progress = models.PositiveIntegerField(default=0)
    # rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    # reviews_count = models.PositiveIntegerField(default=0)
    
    language = models.CharField(max_length=1_000, null=True, blank=True)
    tag = models.TextField(max_length=1_000, null=True, blank=True)
    techs = models.TextField(max_length=10_000, null=True, blank=True)

    # 
    features = models.JSONField(default=list, null=True, blank=True)
    requirements = models.JSONField(default=list, null=True, blank=True)
    target_audience = models.JSONField(default=list, null=True, blank=True)

    is_visible = models.BooleanField(default=True)

 
    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)


    def teach_list(self):
        if self.techs:
            teach_list = self.techs.split(',')
            return teach_list
        return self.techs

    def total_section(self):
        return SectionInCourse.objects.filter(course=self).count()


    def total_lesson(self):
        return LessonInCourse.objects.filter(section__course=self).count()


    def total_enrolled_students(self):
        return StudentCourseEnrollment.objects.filter(course=self).count()


    def course_rating(self):
        course_rating = CourseRating.objects.filter(course=self).aggregate(avg_rating=models.Avg('rating'))
        return course_rating['avg_rating']

    # 
    # old code 
    # @property
    # def lessons_count(self):
    #     count = 0
    #     for section in self.sections.all():
    #         count += section.items.count()
    #     return count
    # @property
    # def lessons_count(self):
    #     return sum(section.items.count() for section in self.sections.all())
    

    # @property
    # def students_count(self):
    #     return self.student_progress.count()
    
    # 
    # old code
    # @property
    # def price_after_discount(self):
    #     """Calculate original price before discount"""
    #     if self.discount > 0:
    #         original = self.price - self.discount
    #         return original
    #     return self.price
    # @property
    def price_after_discount(self):
        return self.price - self.discount
    

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "1-3. Courses"

    def __str__(self):
        return f"{self.id}): ({self.title}) - [{self.user}] - ({self.is_visible})"

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug is None:
            self.slug = slugify(self.title) + "-" + shortuuid.uuid()[:2]

        if self.pk:
            old_instance = Course.objects.get(pk=self.pk)
            if old_instance.image and old_instance.image != self.image:
                default_storage.delete(old_instance.image.path)

        super(Course, self).save(*args, **kwargs)






class SectionInCourse(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='course_sections',
    )

    title = models.CharField(max_length=1_000)

    is_visible = models.BooleanField(default=True) #
    is_free = models.BooleanField(default=False)

    order = models.PositiveIntegerField(default=0)

    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = "1-4. Section In Course"
    
    def total_lesson(self):
        return LessonInCourse.objects.filter(section=self).count()

    def __str__(self):
        return f"{self.id}): ({self.title}) - ({self.is_visible})"






class LessonInCourse(models.Model):
    section = models.ForeignKey(
        SectionInCourse,
        on_delete=models.CASCADE,
        related_name='section_lesson',
    )

    LESSON_TYPES_CHOICES = (
        ('video', 'Video'),
        ('assessment', 'Assessment'),
        ('document', 'Document'),
    )
    type = models.CharField(
        max_length=1_000, 
        choices=LESSON_TYPES_CHOICES,
        default="video",
    )
   
    title = models.CharField(max_length=1_000)
    duration = models.CharField(max_length=1_000, null=True, blank=True)
    description = models.TextField(max_length=10_000, null=True, blank=True)

    # For Video Lessons
    video_file = models.FileField(upload_to="course/lesson/videos", null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)

    # For Question Lessons
    questions = models.JSONField(default=list)

    # For Document Lessons
    content = models.TextField(max_length=10_000, null=True, blank=True)

    # For Files Lessons
    uploaded_files  = models.JSONField(default=list)

    is_visible = models.BooleanField(default=True) #
    is_free = models.BooleanField(default=False)

    order = models.PositiveIntegerField(default=0)

    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "1-5. Lesson In Course"

    def __str__(self):
        return f"{self.id}): [{self.section.course.title}] - [{self.section.title}] - ({self.title}) - ({self.is_visible})"
    

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = LessonInCourse.objects.get(pk=self.pk)
            if old_instance.video_file and old_instance.video_file != self.video_file:
                default_storage.delete(old_instance.video_file.path)

        super(LessonInCourse, self).save(*args, **kwargs)




class FileInCourse(models.Model):
    lesson = models.ForeignKey(
        LessonInCourse,
        on_delete=models.CASCADE,
        related_name='lesson_file',
    )

    name = models.CharField(max_length=1_000, null=True, blank=True)
    file = models.FileField(upload_to="course/lesson/file", null=True, blank=True)
    size = models.PositiveIntegerField(default=0, null=True, blank=True)
    file_type = models.CharField(max_length=1_000, null=True, blank=True)
    
    title = models.CharField(max_length=1_000)
    file_url = models.URLField(null=True, blank=True)

    type = models.CharField(max_length=1_000, null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name_plural = "1-6. File In Course"

    def __str__(self):
        return f"{self.id}): ({self.name})"





class QuestionInCourse(models.Model):
    lesson = models.ForeignKey(
        LessonInCourse,
        on_delete=models.CASCADE,
        related_name='lesson_question',
    )

    QUESTION_TYPES_CHOICES = (
        ('text', 'نص'),
        ('image-url', 'صورة من رابط'),
        ('image-upload', 'صورة مرفوعة'),
    )
    question_type = models.CharField(
        max_length=100, 
        choices=QUESTION_TYPES_CHOICES,
        default="text",
    )
    
    text = models.TextField(max_length=10_000, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    image_file = models.ImageField(upload_to="course/question/images", null=True, blank=True)

    # image_file = models.JSONField(null=True, blank=True)
    
    choices = models.JSONField(default=list)
    correct_answer = models.PositiveIntegerField(default=0)
    
    order = models.PositiveIntegerField(default=0)
    
    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_options(self):
        if isinstance(self.options, str):
            return json.loads(self.options)
        return self.options or []

    class Meta:
        ordering = ['created_at']
        verbose_name_plural="1-7. Question In Course"

    def __str__(self):
        return f"{self.id}): ({self.lesson.title}) - ({self.text[:50]})"


    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = QuestionInCourse.objects.get(pk=self.pk)
            if old_instance.image_file and old_instance.image_file != self.image_file:
                default_storage.delete(old_instance.image_file.path)

        super(QuestionInCourse, self).save(*args, **kwargs)





# ******************************************************************************
# ==============================================================================
# *** Coupon Course *** #
class CouponCourse(models.Model):
    """Coupon model for course discounts"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='coupon_course',
    )

    name = models.CharField(max_length=1_000, unique=True)
    # discount = models.IntegerField(
    #     validators=[MinValueValidator(1), MaxValueValidator(1000)]
    # )
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    usage_limit = models.PositiveIntegerField(
        default=1, 
        null=True, 
        blank=True, 
        help_text="Maximum number of times this coupon can be used.",
    )
    current_usage = models.PositiveIntegerField(
        default=0, 
        null=True, 
        blank=True, 
        help_text="Current number of times this coupon has been used.",
    )

    is_visible = models.BooleanField(default=True)

    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        return self.is_visible and self.current_usage < self.usage_limit

    def decrement_usage(self):
        if self.is_valid():
            self.current_usage += 1
            self.save()
            return True
        return False
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural="1-8. Coupon Course"

    def __str__(self):
        return f"{self.id}): ({self.name}) - ({self.discount}) - ({self.is_visible})"






# ******************************************************************************
# ==============================================================================
# *** Student Course Enrollment *** #
class StudentCourseEnrollment(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrolled_student',
        null=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrolled_courses',
        null=True,
    )

    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        null=True,
        blank=True,
    )

    enrolled_time = models.DateTimeField(auto_now_add=True)

    payment_id = models.CharField(max_length=1_000, null=True, blank=True)
    
    completed = models.BooleanField(default=False)  # إضافة حقل للإكمال
    completion_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # تاريخ الإكمال
    certificate_id = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True) # unique=True

    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:        
        ordering = ['-created_at']
        verbose_name_plural="1-9. Student Enrolled Courses"

    def __str__(self) :
        return f"{self.id}): ({self.course.title}) - ({self.student})"







# ******************************************************************************
# ==============================================================================
# *** Course Rating *** #
class CourseRating(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True,
    )

    STATUS_CHOICES = (
        ("unacceptable", "مرفوض"), 
        ("under-processing", "قيد المعالجة"),
        ("publication", "منشور"),
    )
    status = models.CharField(
        max_length=1_000, 
        choices=STATUS_CHOICES, 
        default="unacceptable",
    )

    rating = models.PositiveBigIntegerField(default=0)
    reviews = models.TextField(max_length=10_000, null=True, blank=True)
    review_time = models.DateTimeField(auto_now_add=True)

    is_visible = models.BooleanField(default=True)
    

    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:        
        ordering = ['-created_at']
        verbose_name_plural="1-10-. Course Ratings"

    def __str__(self):
        return f"{self.id}): ({self.course}) - ({self.student}) - ({self.rating})"







# ******************************************************************************
# ==============================================================================
# *** Student Favorite Course *** #
class StudentFavoriteCourse(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    is_visible = models.BooleanField(default=True)

    
    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural="1-11. Student Favorite Course"

    def __str__(self):
        return f"{self.id}): ({self.course}) - ({self.student})"






# ******************************************************************************
# ==============================================================================
# *** Teacher Student Chat *** #
class TeacherStudentChat(models.Model):
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_chats'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='student_chats'
    )

    msg_to=models.TextField()
    msg_from=models.CharField(max_length=10_000)
    msg_time=models.DateTimeField(auto_now_add=True)
    
    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural="1-12. Teacher Student ChatBot"

    def __str__(self):
        return f"{self.id}): [{self.teacher}] - [{self.student}]"







# ******************************************************************************
# ==============================================================================
# *** Subscribe Course *** #
class SubscribeCourse(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='subscribe_course_user',
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='subscribe_course_course',
    )
    coupon_course = models.ForeignKey(
        CouponCourse, 
        on_delete=models.CASCADE, 
        related_name='subscribe_course_coupon_course',
        null=True,
        blank=True,
    )

    coupon_discount = models.CharField(
        max_length=100_000,
        null=True,
        blank=True, 
    )
    final_price = models.CharField(
        max_length=100_000,
        null=True,
        blank=True, 
    )
    
    # coupon_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    # final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)

    STATUS_CHOICES = (
        ("new", "جديد"),
        ("under-processing", "قيد المعالجة"),
        ("reply", "تم الرد"),
        ("cancel", "تم الألغاء"),
    )
    status = models.CharField(
        max_length=1_000, 
        choices=STATUS_CHOICES, 
        default="new",
    )

    image_url = models.URLField(null=True, blank=True)

    full_name = models.CharField(max_length=1_000)
    email = models.EmailField()

  
    uploaded_files  = models.JSONField(default=list)


    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

 
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural="7-1. Subscribe Course"

    def __str__(self) :
        return f"{self.id}): [{self.user}] - ({self.course})"
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.full_name) + "-" + shortuuid.uuid()[:2]
        super(SubscribeCourse, self).save(*args, **kwargs)
    







# ******************************************************************************
# ==============================================================================
# *** Student Progress Course *** #
# class StudentProgressCourse(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='user_progress')
#     section = models.ForeignKey(SectionInCourse, on_delete=models.CASCADE, null=True, blank=True)
#     lesson = models.ForeignKey(LessonInCourse, on_delete=models.CASCADE, null=True, blank=True)
    
#     # حالة الإكمال
#     is_completed = models.BooleanField(default=False)
#     completed_at = models.DateTimeField(null=True, blank=True)
    
#     # تتبع المشاهدة/القراءة
#     progress_percentage = models.PositiveIntegerField(default=0)
#     last_accessed = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         unique_together = ('user', 'course', 'lesson')
#         ordering = ['-last_accessed']

#     def __str__(self):
#         return f"{self.user.email} - {self.course.title} ({self.progress_percentage}%)"



# ->
class LessonInCourseCompletion(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
    )
    lesson = models.ForeignKey(
        LessonInCourse, 
        on_delete=models.CASCADE,
    )

    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)
        
    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lesson')
        verbose_name_plural="1-14. Lesson In Course Completion"
        
    def __str__(self):
        return f"{self.user.email} - {self.lesson.title}"


class CourseProgress(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
    )

    progress_percentage = models.FloatField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
        
    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'course')
        verbose_name_plural="1-13. Course Progress"
         
    def update_progress(self):
        total_lessons = self.course.lessons_count()
        completed_lessons = LessonInCourseCompletion.objects.filter(
            user=self.user,
            lesson__section__course=self.course,
            is_completed=True
        ).count()
        
        self.progress_percentage = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0
        self.save()





# ******************************************************************************
# ==============================================================================
# *** Student Certificate *** #
class StudentCertificate(models.Model):
    enrollment = models.OneToOneField(
        StudentCourseEnrollment,
        on_delete=models.CASCADE,
        related_name='certificate'
    )

    issued_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='course/certificates/', null=True, blank=True)
    
    issue_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(auto_now_add=True)
    certificate_pdf = models.FileField(upload_to='course/certificates/', null=True, blank=True)
    certificate_url = models.URLField(null=True, blank=True)
    verification_code = models.CharField(max_length=16, unique=True)

    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        verbose_name_plural="1-15. Student Certificate"
         
    def generate_verification_code(self):
        return str(uuid.uuid4().hex)[:16].upper()

    def __str__(self):
        return f"{self.id}): ({self.enrollment.student}) - ({self.enrollment.course})"
    
    def save(self, *args, **kwargs):
        if not self.verification_code:
            self.verification_code = self.generate_verification_code()
        super().save(*args, **kwargs)





# ******************************************************************************
# ==============================================================================
# *** Documents *** #
class Document(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='document_user',
    )
    # admin_profile = models.ForeignKey(
    #     AdminProfile,
    #     on_delete=models.CASCADE,
    #     related_name="admin_profile_document",
    #     null=True,
    #     blank=True,
    # )
    # teacher_profile = models.ForeignKey(
    #     TeacherProfile,
    #     on_delete=models.CASCADE,
    #     related_name="teacher_profile_document",
    #     null=True,
    #     blank=True,
    # )

    section = models.ForeignKey(
        SectionCourse, 
        on_delete=models.CASCADE, 
        related_name='section_course_documents',
        null=True,
        blank=True,
    )
    
    title = models.CharField(max_length=1_000)
    description = models.TextField(max_length=10_000, null=True, blank=True)
    
    image = models.ImageField(upload_to='documents/iamges/', null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    
    # For Files Lessons
    uploaded_files  = models.JSONField(default=list)

    
    is_visible = models.BooleanField(default=True)


    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    # def total_question_in_bank(self):
    #     return QuestionInBank.objects.filter(question_bank=self).count()


    # def total_student_result(self):
    #     return StudentQuestionBankResult.objects.filter(question_bank=self).count()

    # @property
    # def question_count(self):
    #     return self.questions.count()
    
    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url
    

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural="2-1) Documents"
    
    
    def __str__(self):
        return f"{self.id}): ({self.title}) - [{self.user}] - ({self.is_visible})"


    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Document.objects.get(pk=self.pk)
            if old_instance.image and old_instance.image != self.image:
                default_storage.delete(old_instance.image.path)

        super(Document, self).save(*args, **kwargs)










# ******************************************************************************
# ==============================================================================
# *** Questions Banks *** #
class QuestionBank(models.Model):
    """Question bank model containing groups of questions"""
    # section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='question_banks')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='question_banks',
    )
    # admin_profile = models.ForeignKey(
    #     AdminProfile,
    #     on_delete=models.CASCADE,
    #     related_name="admin_profile_question_bank",
    #     null=True,
    #     blank=True,
    # )
    # teacher_profile = models.ForeignKey(
    #     TeacherProfile,
    #     on_delete=models.CASCADE,
    #     related_name="teacher_profile_question_bank",
    #     null=True,
    #     blank=True,
    # )
    section = models.ForeignKey(
        SectionCourse, 
        on_delete=models.CASCADE, 
        related_name='section_course_question_bank',
    )
    
    title = models.CharField(max_length=1_000)
    description = models.TextField(max_length=10_000, null=True, blank=True)
    
    image = models.ImageField(upload_to='questionsbanks/banks/', null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    
    is_visible = models.BooleanField(default=True)

    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def total_question_in_bank(self):
        return QuestionInBank.objects.filter(question_bank=self).count()


    def total_student_result(self):
        return StudentQuestionBankResult.objects.filter(question_bank=self).count()

    @property
    def question_count(self):
        return self.questions.count()
    
    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url
    

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural="2-1) Questions Banks"
    
    
    def __str__(self):
        return f"{self.id}): ({self.title}) - [{self.user}] - ({self.is_visible})"


    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = QuestionBank.objects.get(pk=self.pk)
            if old_instance.image and old_instance.image != self.image:
                default_storage.delete(old_instance.image.path)

        super(QuestionBank, self).save(*args, **kwargs)



class QuestionInBank(models.Model):
    """Question model with text or image"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='question_in_bank',
    )
    question_bank = models.ForeignKey(
        QuestionBank, 
        on_delete=models.CASCADE, 
        related_name='questions_question_in_bank'
    )

    text = models.TextField(max_length=10_000, null=True, blank=True)
    
    image = models.ImageField(upload_to='questionsbanks/questions/', null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
        
    choices = models.JSONField(default=list)
    correct_answer = models.PositiveIntegerField(default=0)
    
    is_visible = models.BooleanField(default=True)

    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural="2-2) Question In Bank"
    
    def __str__(self):
        return f"{self.id}): ({self.text[:50]}) - ({self.is_visible})"


    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = QuestionInBank.objects.get(pk=self.pk)
            if old_instance.image and old_instance.image != self.image:
                default_storage.delete(old_instance.image.path)  
             
        super(QuestionInBank, self).save(*args, **kwargs)



class ChoiceQuestionInBank(models.Model):
    """Answer choices for questions"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='choice_question_in_bank',
    )
    question = models.ForeignKey(
        QuestionInBank, 
        on_delete=models.CASCADE, 
        related_name='choices_question_in_bank',
        # null=True,
        # blank=True,
    )

    text = models.CharField(max_length=1_000)
    is_correct = models.BooleanField(default=False)
        
    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural="2-3) Choice Question In Bank"

    def __str__(self):
        return f"{self.id}): ({self.text[:30]}) - ({self.is_correct})"














# ******************************************************************************
# ==============================================================================
# class StudentQuestionBankResult(models.Model):
#     user = models.ForeignKey(
#         User, 
#         on_delete=models.CASCADE,
#         related_name='student_question_bank_results',
#     )
#     question_bank = models.ForeignKey(
#         QuestionBank, 
#         on_delete=models.CASCADE,
#         related_name='question_bank_bank_result',
#     )

#     answered_questions = models.PositiveIntegerField()
#     correct_answers = models.PositiveIntegerField()
#     percentage = models.FloatField()
#     total_questions = models.PositiveIntegerField()


#     slug = models.SlugField(unique=True, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
#     updated_at = models.DateTimeField(auto_now=True)


#     class Meta:
#         ordering = ['-created_at']
#         verbose_name_plural="2-4) Student Question Bank Result"
   

#     def __str__(self):
#         return f"{self.id}): ({self.user}) - ({self.question_bank})"
    

# class StudentQuestionBankAnswer(models.Model):
#     question_bank_result = models.ForeignKey(
#         StudentQuestionBankResult, 
#         on_delete=models.CASCADE,
#         related_name='question_bank_answers', 
#     )

#     question_id = models.PositiveIntegerField()
#     question_text = models.TextField()

#     is_answered = models.BooleanField()
    
#     selected_choice_id = models.PositiveIntegerField(null=True, blank=True)
#     selected_choice_text = models.TextField(null=True, blank=True)
#     correct_choice_id = models.PositiveIntegerField(null=True, blank=True)
#     correct_choice_text = models.TextField(null=True, blank=True)
    
#     is_correct = models.BooleanField(null=True, blank=True)
#     all_choices = models.JSONField(default=list)

#     slug = models.SlugField(unique=True, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-created_at']
#         verbose_name_plural="2-5) Student Question Bank Answer"
   
#     def __str__(self):
#         return f"{self.id}): ({self.question_text})" 







# ******************************************************************************
# ==============================================================================
# ***  Student Question Bank Result  *** // 
class StudentQuestionBankResult(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='student_question_bank_results',
    )
    question_bank = models.ForeignKey(
        QuestionBank, 
        on_delete=models.CASCADE,
        related_name='question_bank_bank_result',
    )

    # answered_questions = models.PositiveIntegerField()
    
    total_questions = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField()
    percentage = models.FloatField()

    results = models.JSONField(default=list)


    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_at']
        verbose_name_plural="2-4) Student Question Bank Result"
   

    def __str__(self):
        return f"{self.id}): ({self.user}) - ({self.question_bank}) - [{self.user}]"
    










# ******************************************************************************
# ==============================================================================
# ***    *** #









# ******************************************************************************
# ==============================================================================
# ***  ContactUs  *** #
class ContactUsUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,        
        related_name='contactus_user',
        null=True,
        blank=True,
    )

    STATUS_CHOICES = (
        ("new", "جديد"),
        ("under-processing", "قيد المعالجة"),
        ("reply", "تم الرد"),
    )
    status = models.CharField(
        max_length=1_000, 
        choices=STATUS_CHOICES, 
        default="new",
    )

    full_name = models.CharField(max_length=1_000)
    email = models.EmailField()

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

    titleofmessage = models.CharField(max_length=1_000)
    message = models.TextField(
        max_length=10_000, 
        null=True, 
        blank=True,
    )

    quick_reply = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)

    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}): ({self.titleofmessage}) - ({self.status}) - ({self.is_visible})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "3-1] ContactUs"

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.titleofmessage) + "-" + shortuuid.uuid()[:2]
        super(ContactUsUser, self).save(*args, **kwargs)







# ******************************************************************************
# ==============================================================================
# ***  Review  *** #
class ReviewUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviewuser_user',
    )
    profile = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='reviewuser_profile',
    )

    STATUS_CHOICES = (
        ("unacceptable", "مرفوض"), 
        ("under-processing", "قيد المعالجة"),
        ("publication", "منشور"),
    )
    status = models.CharField(
        max_length=1_000, 
        choices=STATUS_CHOICES, 
        default="publication",
        null=True,
        blank=True,
    )

    first_name = models.CharField(max_length=1_000)
    message = models.TextField(
        max_length=10_000, 
        null=True, 
        blank=True,
    )
    rating = models.PositiveBigIntegerField(default=0)
    # rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])

    is_visible = models.BooleanField(default=True)

    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}): ({self.first_name}) - ({self.status}) - ({self.is_visible})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "3-2] Review User"

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.first_name) + "-" + shortuuid.uuid()[:2]
        super(ReviewUser, self).save(*args, **kwargs)







# ******************************************************************************
# ==============================================================================
# ***  *** #
# class CategoryPost(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#     ) 

#     title = models.CharField(max_length=1_000)
#     description = models.TextField(max_length=10_000, null=True, blank=True)
#     image = models.ImageField(upload_to="category", null=True, blank=True)

#     # view = models.IntegerField(default=0)
#     view = models.PositiveIntegerField(default=0)
#     likes = models.ManyToManyField(User, related_name="likes_category", blank=True,)

#     slug = models.SlugField(unique=True, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.id}): ({self.title})"

#     class Meta:
#         verbose_name_plural = "Category"

#     def save(self, *args, **kwargs):
#         if self.slug == "" or self.slug == None:
#             self.slug = slugify(self.title) + "-" + shortuuid.uuid()[:2]
#         super(Category, self).save(*args, **kwargs)

# class Post(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts',)
#     category = models.ForeignKey(
#         Category,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name="Post",
#     )

#     title = models.CharField(max_length=1_000)
#     description = models.TextField(max_length=10_000)
    
#     views = models.PositiveIntegerField(default=0)
#     likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.id}): ({self.title})"

# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments',)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',)

#     text = models.TextField(max_length=10_000)
#     likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Comment by: ({self.user.username} on {self.post.title})"

# class Reply(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies',)
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies',)

#     text = models.TextField(max_length=10_000)
#     likes = models.ManyToManyField(User, related_name='liked_replies', blank=True,)
    
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Reply by: ({self.user.username} on {self.comment.text})"

# class Notification(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications',)

#     NOTIFICATION_TYPES = [
#         ('like_post', 'Like Post'),
#         ('like_comment', 'Like Comment'),
#         ('like_reply', 'Like Reply'),
#         ('comment', 'Comment'),
#         ('reply', 'Reply'),
#         ('report', 'Report'),
#     ]
#     notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)

    
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True,)
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True,)
#     reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True,)
    
#     message = models.CharField(max_length=1_000)
#     is_read = models.BooleanField(default=False)
    
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.id}): ({self.message})"

# class Report(models.Model):
#     REPORT_REASONS = [
#         ('spam', 'Spam'),
#         ('inappropriate', 'Inappropriate Content'),
#         ('harassment', 'Harassment'),
#         ('other', 'Other'),
#     ]
#     reason = models.CharField(max_length=50, choices=REPORT_REASONS)

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports',)

#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports',)
#     details = models.TextField(blank=True, null=True)
    
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Report by: ({self.user.username} on {self.post.title})"

# ==============================================================================
# ***  *** #