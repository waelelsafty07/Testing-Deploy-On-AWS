

import random
from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from server import settings
from authentication.models import EmailConfirm
from users.models import Users


@shared_task
def send_reset_password_mail_task(reset_password_token):
    key = reset_password_token['key']
    email_plaintext_message = "{}?token={}".format(
        reverse('password_reset:reset-password-request'), key)

    send_mail(
        subject='Reset Password!',
        message=email_plaintext_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["waelelsafty07@gmail.com", ],
        fail_silently=False,
    )
    print('Email sent successfully')
    return f'Email sent successfully'


@shared_task
def send_Confirm_mail_task(user_id):
    user = Users.objects.get(id=user_id)
    otp = random.randint(100000, 999999)
    key = make_password(str(otp))
    EmailConfirm.objects.create(key=key, user=user)
    send_mail(
        subject='Congratulations!',
        message=f'Thank you for registration.\n\
            Welcome {user.username} To activate Your Account use this OTP: {otp}\n\
            Best Regards\n Bee Team ',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["waelelsafty07@gmail.com", ],
        fail_silently=False,
    )
    return f'Email sent successfully'
