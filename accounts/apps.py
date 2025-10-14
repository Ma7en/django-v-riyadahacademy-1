# 
from django.apps import AppConfig


# 
class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    # def ready(self):
    #     # استيراد ملف الإشارات لضمان تسجيلها عند بدء تشغيل التطبيق
    #     import accounts.signals
