#
import shortuuid


#
from django.db import models
from django.db import models
from django.utils.text import slugify


# 
from accounts.models import *



# Create your models here.
# =================================================================
# *** Category Section *** #
class CategorySection(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='category_section',
    )

    title=models.CharField(max_length=1_000)
    description=models.TextField(
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
    
    is_hidden = models.BooleanField(default=False)

    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural="2. Categories Sections"

    def total_category_section(self):
        return SectionCourse.objects.filter(category=self).count()

    def __str__(self) :
        return f"{self.id}): ({self.title})"
    
# =================================================================
# *** Section Course *** #
class SectionCourse(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='section_course',
    )
    category=models.ForeignKey(
        CategorySection, 
        on_delete=models.CASCADE, 
        related_name='category_section',
    )

    title=models.CharField(max_length=1_000)
    description=models.TextField(
        max_length=10_000, 
        null=True, 
        blank=True,
    )
    grade=models.CharField(max_length=1_000)
    
    image = models.ImageField(
        upload_to="sectioncourse", 
        null=True,
        blank=True,
    )
    image_url = models.URLField(null=True, blank=True)

    is_hidden = models.BooleanField(default=False)

    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural="3. Section Course"

    def __str__(self) :
        return f"{self.id}): ({self.title})"
    
    
# =================================================================
# *** Course *** #
# class Course(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='courses',
#     )

#     title = models.CharField(max_length=1_000)
#     description = models.TextField(max_length=10_000, null=True, blank=True)
#     image = models.ImageField(upload_to="courses", null=True, blank=True)
#     image_url = models.URLField(null=True, blank=True)
#     duration = models.CharField(max_length=100, null=True, blank=True)
#     lesson_count = models.PositiveIntegerField(default=0)
#     students_count = models.PositiveIntegerField(default=0)
#     progress = models.PositiveIntegerField(default=0)
#     price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
#     reviews_count = models.PositiveIntegerField(default=0)
#     last_updated = models.CharField(max_length=100, null=True, blank=True)
#     language = models.CharField(max_length=100, null=True, blank=True)
#     level = models.CharField(max_length=100, null=True, blank=True)
#     category = models.CharField(max_length=100, null=True, blank=True)
#     tag = models.CharField(max_length=100, null=True, blank=True)
#     features = models.JSONField(default=list, null=True, blank=True)
#     requirements = models.JSONField(default=list, null=True, blank=True)
#     target_audience = models.JSONField(default=list, null=True, blank=True)

#     slug = models.SlugField(unique=True, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.id}): ({self.title})"

#     class Meta:
#         verbose_name_plural = "4. Courses"

#     def save(self, *args, **kwargs):
#         if self.slug == "" or self.slug is None:
#             self.slug = slugify(self.title) + "-" + shortuuid.uuid()[:2]
#         super(Course, self).save(*args, **kwargs)


# class Instructor(models.Model):
#     course = models.ForeignKey(
#         Course,
#         on_delete=models.CASCADE,
#         related_name='instructors',
#     )

#     name = models.CharField(max_length=1_000)
#     title = models.CharField(max_length=1_000, null=True, blank=True)
#     bio = models.TextField(max_length=10_000, null=True, blank=True)
#     image = models.ImageField(upload_to="instructors", null=True, blank=True)
#     image_url = models.URLField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.id}): ({self.name})"


# class Section(models.Model):
#     course = models.ForeignKey(
#         Course,
#         on_delete=models.CASCADE,
#         related_name='sections',
#     )

#     title = models.CharField(max_length=1_000)
#     is_visible = models.BooleanField(default=True)
#     is_free = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.id}): ({self.title})"


# class Item(models.Model):
#     ITEM_TYPES = (
#         ('video', 'Video'),
#         ('assessment', 'Assessment'),
#     )
#     section = models.ForeignKey(
#         Section,
#         on_delete=models.CASCADE,
#         related_name='items',
#     )

#     title = models.CharField(max_length=1_000)
#     type = models.CharField(max_length=100, choices=ITEM_TYPES)
#     duration = models.CharField(max_length=100, null=True, blank=True)
#     url = models.URLField(null=True, blank=True)
#     description = models.TextField(max_length=10_000, null=True, blank=True)
#     is_visible = models.BooleanField(default=True)
#     is_free = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.id}): ({self.title})"


# class File(models.Model):
#     item = models.ForeignKey(
#         Item,
#         on_delete=models.CASCADE,
#         related_name='files',
#     )

#     name = models.CharField(max_length=1_000)
#     size = models.PositiveIntegerField(default=0)
#     type = models.CharField(max_length=100)
#     url = models.URLField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.id}): ({self.name})"


# class Question(models.Model):
#     QUESTION_TYPES = (
#         ('text', 'Text'),
#         ('image-url', 'Image URL'),
#         ('image-upload', 'Image Upload'),
#     )
#     item = models.ForeignKey(
#         Item,
#         on_delete=models.CASCADE,
#         related_name='questions',
#     )

#     question_type = models.CharField(max_length=100, choices=QUESTION_TYPES)
#     text = models.TextField(max_length=10_000, null=True, blank=True)
#     image_url = models.URLField(null=True, blank=True)
#     image_file = models.JSONField(null=True, blank=True)
#     options = models.JSONField(default=list)
#     correct_answer = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return f"{self.id}): ({self.text[:50]})"

# =================================================================
# *** ContactUs *** #
class ContactUsUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,        
        related_name='contactus_user',
    )

    full_name = models.CharField(max_length=1_000)
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex="^01[0|1|2|5][0-9]{8}$",
                message="Phone must be start 010, 011, 012, 015 and all number contains 11 digits",
            )
        ],
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
    is_hidden = models.BooleanField(default=False)
    STATUS = (
        ("جديد", "جديد"),
        ("قيد المعالجة", "قيد المعالجة"),
        ("تم الرد", "تم الرد"),
    )
    status = models.CharField(
        max_length=1_000, 
        choices=STATUS, 
        default="جديد",
    )


    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}): ({self.titleofmessage})"
    
    class Meta:
        verbose_name_plural = "ContactUs"

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.titleofmessage) + "-" + shortuuid.uuid()[:2]
        super(ContactUsUser, self).save(*args, **kwargs)


# =================================================================
# *** Review *** #
class ReviewUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    # course=models.ForeignKey(
    #     Course,
    #     on_delete=models.CASCADE,
    #     null=True,
    # )

    first_name = models.CharField(max_length=1_000)
    message = models.TextField(
        max_length=10_000, 
        null=True, 
        blank=True,
    )
    rating=models.PositiveBigIntegerField(default=0)
    # rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    is_hidden = models.BooleanField(default=False)
    STATUS = (
        ("مرفوض", "مرفوض"), 
        ("قيد المعالجة", "قيد المعالجة"),
        ("منشور", "منشور"),
    )
    status = models.CharField(
        max_length=1_000, 
        choices=STATUS, 
        default="مرفوض",
    )

    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}): ({self.first_name})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Review"

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.first_name) + "-" + shortuuid.uuid()[:2]
        super(ReviewUser, self).save(*args, **kwargs)


# =================================================================
# ***  *** #
# class Category(models.Model):
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
#     created_at = models.DateTimeField(auto_now_add=True)
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

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.id}): ({self.title})"

# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments',)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',)

#     text = models.TextField(max_length=10_000)
#     likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Comment by: ({self.user.username} on {self.post.title})"

# class Reply(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies',)
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies',)

#     text = models.TextField(max_length=10_000)
#     likes = models.ManyToManyField(User, related_name='liked_replies', blank=True,)
    
#     created_at = models.DateTimeField(auto_now_add=True)
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
    
#     created_at = models.DateTimeField(auto_now_add=True)
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
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Report by: ({self.user.username} on {self.post.title})"

# =================================================================
# ***  *** #