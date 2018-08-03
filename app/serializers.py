from .models import *
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers, exceptions
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from random import randint
from django.utils import timezone
from datetime import timedelta


UserModel = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'url')


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.CharField()
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    location = serializers.CharField(source='profile.location', read_only=True)
    role = serializers.BooleanField(source='profile.role', read_only=True)

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'last_name', 'first_name', 'location', 'role',)


class UserProfileSerializer(RegisterSerializer):
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    username = serializers.CharField(source='user.username')
    location = serializers.CharField(required=True)
    role = serializers.BooleanField()

    def custom_signup(self, request, user):
        profile = Profile()
        params = request._data
        user = User()
        user.email = params.get('email', '')
        user.username = params.get('username', '')
        user.first_name = params.get('first_name', '')
        user.last_name = params.get('last_name', '')
        user.save()
        user.set_password(params.get('password1', ''))
        user.save()
        profile.location = params.get('location', '')
        profile.role = params.get('role', '')
        profile.user = user
        profile.save()
        return profile


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    freelancer = serializers.ReadOnlyField(source='freelancer.email')
    freelancer_name = serializers.CharField(source='freelancer.get_username', read_only=True)

    class Meta:
        model = Offer
        fields = ('delivery_time', 'price', 'details', 'project', 'freelancer', 'freelancer_name',)


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    offers = OfferSerializer(many=True, read_only=True)
    employer = serializers.ReadOnlyField(source='employer.email')
    employer_name = serializers.CharField(source='employer.get_username', read_only=True)
    location = serializers.ChoiceField(choices=LOCATION_CHOICES)
    publish_date = serializers.DateTimeField(format='%d/%m/%Y, %H:%M', read_only=True)

    class Meta:
        model = Project
        fields = ('title', 'description', 'location', 'publish_date', 'budget', 'category', 'category_name', 'offers', 'employer', 'employer_name', 'url',)


class ResetSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        """ Override this method to change default e-mail options
        """
        return {}

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        if not UserModel.objects.filter(email=value).exists():
            raise exceptions.ValidationError(_('No user is registered with this e-mail address'))

        return value

    def save(self):
        token = randint(1000, 99999)
        user = User.objects.filter(email=self.validated_data.get('email', '')).first()
        resettoken, created = ResetToken.objects.update_or_create(user=user)
        resettoken.user = user
        resettoken.token_reset = token
        resettoken.created = timezone.now()
        resettoken.save()

        text_message = 'this is the text message :'+ str(token)
        send_mail('Reset Password', text_message, 'from@admin.com', self.validated_data.values(), fail_silently=False)
        return resettoken


class PasswordResetConfirmSerializer(serializers.Serializer):

    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    token = serializers.CharField(required=True)

    set_password_form_class = SetPasswordForm

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        self._errors = {}

        if not ResetToken.objects.filter(token_reset=attrs['token']).exists():
            raise exceptions.ValidationError({'token': 'Invalid token'})

        reset_token = ResetToken.objects.filter(token_reset=attrs['token']).first()

        if reset_token.created < timezone.now() - timedelta(days=1):
            raise exceptions.ValidationError({'token': 'Token expired'})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=reset_token.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs

    def save(self):
        self.set_password_form.save()


class ResetTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResetToken
        fields = ('id','token_reset','user', 'created')