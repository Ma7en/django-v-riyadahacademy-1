# accounts/permissions.py

from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import User

class IsTokenValid(BasePermission):
    """
    يتحقق مما إذا كان مفتاح التوكن الموجود في الـ JWT مطابقًا للمفتاح الحالي في قاعدة بيانات المستخدم.
    هذا يضمن أن التوكنات القديمة (من جلسات أخرى) تصبح غير صالحة.
    """
    message = 'This token is no longer valid. Session has expired from another device.'

    def has_permission(self, request, view):
        # --- جملة طباعة للتشخيص ---
        print("\n[DEBUG] IsTokenValid Permission: CHECKING NOW...")
        # ---------------------------

        # هذا الـ permission يجب أن يعمل فقط للمستخدمين المسجلين
        if not request.user or not request.user.is_authenticated:
            print("[DEBUG] IsTokenValid: User is not authenticated. Skipping check.")
            # نرجع True لأن IsAuthenticated سيتعامل مع رفض الطلب بالفعل
            return True

        # request.auth هو المكان الذي يخزن فيه DRF Simple JWT الـ payload للتوكن
        token_payload = request.auth
        if not token_payload:
            print("[DEBUG] IsTokenValid: Could not find token payload (request.auth). Request DENIED.")
            return False

        # استخراج المفتاح من بيانات التوكن
        token_key = token_payload.get('jwt_token_key')

        if not token_key:
            print("[DEBUG] IsTokenValid: 'jwt_token_key' not found in token payload. Allowing request for compatibility.")
            # اسمح بالمرور للتوافق مع التوكنات القديمة التي لا تحتوي على المفتاح
            return True

        try:
            # دائماً احصل على أحدث نسخة من المستخدم من قاعدة البيانات
            user_from_db = User.objects.get(id=request.user.id)
            db_key = str(user_from_db.jwt_token_key)
            
            # --- جمل طباعة للتشخيص ---
            print(f"[DEBUG] IsTokenValid: User: {request.user.email}")
            print(f"[DEBUG] IsTokenValid: Key from TOKEN:   {token_key}")
            print(f"[DEBUG] IsTokenValid: Key from DATABASE: {db_key}")
            # ---------------------------

            is_match = (db_key == token_key)
            
            if is_match:
                print("[DEBUG] IsTokenValid: Keys MATCH. Request ALLOWED.")
            else:
                print("[DEBUG] IsTokenValid: Keys DO NOT MATCH. Request DENIED.")

            return is_match

        except User.DoesNotExist:
            print(f"[DEBUG] IsTokenValid: User with id {request.user.id} does not exist in DB. Request DENIED.")
            return False

