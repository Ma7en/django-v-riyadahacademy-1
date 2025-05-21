#
from rest_framework import serializers


# 
from cores import models


# *****************************************************************
# =================================================================
# *** ContactUs *** #
class ContactUsUserSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.ContactUsUser
        fields = "__all__"


# *****************************************************************
# =================================================================
# *** Review *** #
class ReviewUserSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = models.ReviewUser
        fields = "__all__"


# *****************************************************************
# =================================================================
# ***  *** #

class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    view = serializers.IntegerField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Category
        fields = "__all__"

    def get_likes_count(self, obj):
        return obj.likes.count()

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    view = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Post
        fields = "__all__"
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
class CommentSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Comment
        fields = "__all__"
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    

class ReplySerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Reply
        fields = "__all__"

    def get_likes_count(self, obj):
        return obj.likes.count()

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = "__all__"


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Report
        fields = "__all__"


# *****************************************************************
# =================================================================
# ***  *** #