# 
from django.contrib.sessions.models import Session
from django.utils import timezone



# 
class PreventConcurrentLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            session_key = request.session.session_key
            if request.user.logged_in_user_session_key and request.user.logged_in_user_session_key != session_key:
                # تسجيل الخروج من الجلسة القديمة
                try:
                    s = Session.objects.get(session_key=request.user.logged_in_user_session_key)
                    s.delete()
                except Session.DoesNotExist:
                    pass  # لا يوجد جلسة قديمة

            # تحديث مفتاح الجلسة الحالي للمستخدم
            request.user.logged_in_user_session_key = session_key
            request.user.save()

        response = self.get_response(request)
        return response



