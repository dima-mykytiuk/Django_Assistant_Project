from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from django.conf import settings

from users.models import Profile


def send_email_for_verify(request, user):
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    }
    if Profile.objects.filter(user=user).exists() is False:
        Profile.objects.create(user=user, email_confirmed=False)
    message = render_to_string(
        'email_notifications/verify_email.html',
        context=context,
    )
    email = EmailMessage(
        'Verify email',
        message,
        from_email=settings.EMAIL_FROM_USER,
        to=[user.email],
    )
    email.send()
    