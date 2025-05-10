import logging
import time

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from celery import shared_task
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)
User = get_user_model()
@shared_task(bind=True)
def send_verification_email(self, user_id, user_email):
    try:

        receiver_email = user_email
        template_name = 'verification.html'
        convert_to_html_content = render_to_string(
            template_name=template_name,
            context={'user': user_id}
        )
        plain_message = strip_tags(convert_to_html_content)
        print('')
        send_mail(
            subject="Verification Email",
            message=plain_message,
            from_email = 'app.social@email.com',
            recipient_list=[receiver_email,],
            fail_silently=False,
        )
        print('email sent')
    except Exception as e:
        print(e)
        raise e