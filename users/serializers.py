from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator
from .utils import send_email_for_verify
from .models import User, Profile


class EmailConfirmed(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ('email_confirmed',)


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=False, style={'input_type': 'password'})
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    email_confirmed = EmailConfirmed(required=False, default=False)
    
    def create(self, validated_data):
        if 'password' in validated_data:
            user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                email=validated_data['email'],
                is_superuser=validated_data['is_superuser'],
                is_staff=validated_data['is_staff'],
            )
            if validated_data['email_confirmed']:
                Profile.objects.create(user=user, email_confirmed=True)
            else:
                send_email_for_verify(self.context.get('request'), user)
            return user
        else:
            raise serializers.ValidationError("Password field may not be blank when you create new user")
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        if validated_data.get('password'):
            instance.password = make_password(validated_data.get('password', instance.password))
        if validated_data.get('email_confirmed'):
            if Profile.objects.filter(user=instance).exists():
                profile = Profile.objects.get(user=instance)
                profile.email_confirmed = True
                profile.save()
            else:    
                Profile.objects.create(user=instance, email_confirmed=True)
        else:
            if Profile.objects.filter(user=instance).exists():
                profile = Profile.objects.get(user=instance)
                profile.email_confirmed = False
                profile.save()
            else:
                Profile.objects.create(user=instance, email_confirmed=False)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ("id", "username", "password", 'email', 'is_superuser', 'is_staff', 'email_confirmed')
