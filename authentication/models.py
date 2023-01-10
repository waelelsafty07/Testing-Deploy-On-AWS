from django.db import models

from users.models import Users

from django_rest_passwordreset.signals import reset_password_token_created


class EmailConfirm(models.Model):
    key = models.CharField(max_length=128, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        Users,
        related_name='email_confirm_tokens',
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'email_confirm'

