from datetime import datetime, timezone
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password, make_password
from authentication.models import EmailConfirm
from rest_framework.validators import UniqueValidator

from rest_framework import serializers
from users.models import Users
from .tasks import send_Confirm_mail_task


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'passwordConfirm']

    username = serializers.CharField(required=True, validators=[
                                     UniqueValidator(queryset=Users.objects.all())])
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=Users.objects.all())])
    password = serializers.CharField(
        required=True, write_only=True, validators=[validate_password])
    passwordConfirm = serializers.CharField(
        required=True, write_only=True, validators=[validate_password])

    def validate(self, data):
        if data['password'] != data['passwordConfirm']:
            raise serializers.ValidationError("password not confirmed.")
        return data

    def create(self, validated_data):
        user = Users(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.set_password(validated_data['passwordConfirm'])

        user.save()
        send_Confirm_mail_task.delay(user.id)
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        message = {
            'status': 'success',
            'message': 'Go to activate your account with Email Confirmation.',
            'redirect': True
        }
        if not user:
            raise serializers.ValidationError(
                {'status': 'failed', 'message': 'Incorrect Credentials Passed.'})
        if user and not user.email_confirm and user.is_active:
            message = {
                'status': 'success',
                'message': 'Go to activate your account with Email Confirmation.',
                'redirect': False
            }
            return user, message
        if user and not user.is_active:
            user.is_active = True
            user.save()
            message = "Welcome Back to our app we so happy for you to comback again"
            return [user, message]

        return user, message

    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'bio', 'is_active', 'password']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', "email", "is_staff",
                  'first_name', 'last_name', 'last_login']


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'password', 'passwordConfirm', 'old_password']
    username = serializers.CharField(required=False)
    old_password = serializers.CharField(
        required=True, write_only=True, validators=[validate_password])
    password = serializers.CharField(
        required=True, write_only=True, validators=[validate_password])
    passwordConfirm = serializers.CharField(
        required=True, write_only=True, validators=[validate_password])

    def validate(self, data):
        if data['password'] and data['passwordConfirm'] and data['old_password'] and len(data) == 3:
            if not check_password(data['old_password'], self.instance.password):
                raise serializers.ValidationError("old password not correct.")
            if data['password'] != data['passwordConfirm']:
                raise serializers.ValidationError("password not confirmed.")
        else:
            raise serializers.ValidationError(
                "This route for update only paassword.")
        return data

    def update(self, instance, validated_data):

        user = Users.objects.get(pk=instance.id)
        user.password = make_password(validated_data['password'])
        user.save()
        return user


class ConfirmEmailSerializer(serializers.ModelSerializer):

    otp = serializers.CharField(required=True, max_length=6, min_length=6)
    username = serializers.CharField(required=False)
    password = serializers.CharField(
        required=False)

    class Meta:
        model = Users
        fields = "__all__"

    def validate(self, data):
        # check_password(data['otp'], self.instance.password)
        try:
            email_confirm = EmailConfirm.objects.filter(
                user=self.instance).latest('created_at')
            time = datetime.now(timezone.utc) - email_confirm.created_at
            seconds = time.total_seconds()
            if seconds >= 15*60:
                raise serializers.ValidationError(
                    "Time Expire.")
            if not check_password(data['otp'], email_confirm.key):
                raise serializers.ValidationError(
                    "OTP Not Valid.")

            return data

        except EmailConfirm.DoesNotExist:
            raise serializers.ValidationError(
                "User Not Found.")

    def update(self, instance, validated_data):

        user = Users.objects.get(pk=instance.id)
        user.email_confirm = True
        EmailConfirm.objects.filter(user=instance.id).delete()
        user.save()
        return user
