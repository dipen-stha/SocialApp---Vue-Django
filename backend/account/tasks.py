import logging
from decouple import config

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

from celery import shared_task
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from account.models import Email

logger = logging.getLogger(__name__)
User = get_user_model()
@shared_task(bind=True)
def send_verification_email(self, user_id: int, user_email: str):
    try:

        receiver_email = user_email
        email = Email.objects.get(email=user_email)
        template_name = 'verification.html'
        html_content = render_to_string(
            template_name=template_name,
            context={
                'user': user_id,
                'frontend_url': config('FRONTEND_URL'),
                'token': email.verification_token
            }
        )
        msg = EmailMultiAlternatives(
            subject="Verify Your Email",
            body="Please verify your email",
            from_email="noreply@socialapp.com",
            to=[receiver_email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    except Exception as e:
        print(e)
        raise e