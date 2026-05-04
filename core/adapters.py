from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Skip signup if the email already exists
        if sociallogin.is_existing:
            return

        # If the email exists but isn't linked yet, link it automatically
        email = sociallogin.user.email
        if email:
            try:
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass
