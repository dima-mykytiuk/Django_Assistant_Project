from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import info
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from .forms import SignUpForm, LoginForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from .utils import send_email_for_verify
from .models import Profile
# Create your views here.


class IndexView(View):
    template_name = 'pages/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'title': 'Web assistant'})


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        profile = Profile.objects.create(user_id=user.id)
        if user is not None and token_generator.check_token(user, token):
            profile.email_confirmed = True
            profile.save()
            user.save()
            login(request, user)
            return redirect('index')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user


class RegistrationView(View):
    form_class = SignUpForm
    template_name = 'pages/registration.html'
    
    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            send_email_for_verify(request, user)
            return redirect('confirm_email')
        context = {
            'form': form
        }
        
        return render(request, self.template_name, context=context)


class LoginView(View):
    form_class = LoginForm
    template_name = 'pages/login.html'
    
    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user and check_password(password, user.password):
                profile = Profile.objects.filter(user_id=user.id)
                if len(profile) > 0:
                    login(request, user)
                    return redirect('index')
                else:
                    send_email_for_verify(self.request, user)
                    info(request, 'Email not verify, check your email')
            else:
                info(request, 'Username or password is incorrect')
        
        return render(request, self.template_name, {'form': form})


class LogOutView(LoginRequiredMixin, View):
    
    @staticmethod
    def get(request, *args, **kwargs):
        logout(request)
        return redirect('index')
    