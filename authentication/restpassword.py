
from authentication.serializers import UserSerializer
from django_rest_passwordreset.signals import reset_password_token_created

from django.dispatch import receiver
from authentication.tasks import send_reset_password_mail_task


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    user = UserSerializer(reset_password_token.user)
    jsonData = {
        "key": reset_password_token.key,
        "user": user.data
    }
    send_reset_password_mail_task.delay(jsonData)
