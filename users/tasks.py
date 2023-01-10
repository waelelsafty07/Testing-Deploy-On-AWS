import random
from celery import shared_task
from django.core.mail import send_mail
from server import settings
from django.apps import apps
from django.contrib.auth.hashers import check_password, make_password

from authentication.models import EmailConfirm


