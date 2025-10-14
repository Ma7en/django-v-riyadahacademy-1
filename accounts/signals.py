# 
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


# 
# from . import models
from .models import User


# 
@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    user = kwargs.get('user')
    user.logged_in_user_session_key = request.session.session_key
    user.save()


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    user = kwargs.get('user')
    if user:
        user.logged_in_user_session_key = None
        user.save()
