import os, hashlib, logging

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.crypto import get_random_string

from myauth.forms import UserCreationForm, ConfirmRegistrationForm, LoginForm, ResetPasswordForm, ConfirmPasswordResetForm, ChangePasswordForm
from myauth.models import RegistrationCode, ResetPasswordCode

from noteapp import mail_utils

logger = logging.getLogger(__name__)

def login_view(request):
    """Render the login form and handle user authentication."""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(username=form.cleaned_data['username']).first()
            if user and not user.is_active:
                logger.warning(f"Inactive user attempted login: {user.username}")
                messages.info(request, 'Your account is not active. Please confirm your registration (check your email).')
                return redirect('confirm_registration')

            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect("note_list")
            else:
                logger.warning(
                    "Failed login attempt",
                    extra={"username": form.cleaned_data.get("username")}
                )
                form.add_error(None, "Invalid username or password.")

    else:
        form = LoginForm()

    return render(
        request, 'myauth/login.html', {'form': form, 'title': 'Login'})


def register_view(request):
    """Render the registration form and handle user registration."""
    if request.method == 'POST':
        logging.info("Processing registration form submission")
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            code = RegistrationCode.objects.create(
                code=get_random_string(length=6),
                user=user
            )
            mail_utils.send_registration_code(user.email, code.code)
            logger.info(f"Created registration code for user {user.username}")
            messages.success(request, 'Check your inbox for the registration code: ' + code.code)
            return redirect('confirm_registration')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'myauth/register.html', {'form': form, 'title': 'Register'})


def confirm_registration(request):
    """Confirm the registration using the code sent to the user's email."""
    if request.method == 'POST':
        form = ConfirmRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            confirmation_code = form.cleaned_data['confirmation_code']
        
            user = User.objects.get(email=email)
            code = RegistrationCode.objects.get(user=user, code=confirmation_code)
            if code:
                logger.info(f"Activating user {user.username}")
                user.is_active = True
                user.save()
                code.delete()
                messages.success(request, 'Registration confirmed! Please log in now.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid confirmation code.')
    else:
        form = ConfirmRegistrationForm()
    
    return render(request, 'myauth/confirm_registration.html', {'form': form, 'title': 'Confirm Registration'})


def reset_password_view(request):
    """Render the reset password form and handle password reset requests."""
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                code = ResetPasswordCode.objects.filter(user=user).first()
                if code and is_expired(code.created_at):
                    code.delete()

                if not code or not is_expired(code.created_at):
                    logger.info(f"Sending password reset code to {email}")
                    reset_code = get_random_string(length=6)
                    ResetPasswordCode.objects.create(code=reset_code, user=user)
                    mail_utils.send_password_reset(user.email, reset_code)
                    messages.success(request, 'Check your inbox for the password reset code.')
                    return redirect('confirm_password_reset')
                else:
                    messages.error(request, 'A reset code has already been sent. Please check your email or wait 10 minutes to ask for a new one.')
            else:
                logger.warning(f"Password reset attempt for non-existent email: {email}")
                messages.error(request, 'No user found with that email address.')

    else:
        form = ResetPasswordForm()
    
    return render(request, 'myauth/reset_password.html', {'form': form, 'title': 'Reset Password'})


def confirm_password_reset_view(request):
    """Confirm the password reset form using the code sent to the user's email."""
    if request.method == 'POST':
        form = ConfirmPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            reset_code = form.cleaned_data['reset_code']
            new_password = form.cleaned_data['new_password']
            repeat_password = form.cleaned_data['repeat_password']
            if new_password != repeat_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('confirm_password_reset')
            
            user = User.objects.filter(email=email).first()
            code = ResetPasswordCode.objects.filter(code=reset_code, user=user).first()
            if code:
                logger.info(f"Setting new password for user {user.username} with password {new_password}")
                user.set_password(new_password)
                user.save()
                code.delete()
                messages.success(request, 'Password reset successful! Please log in now.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid reset code.')
    else:
        form = ConfirmPasswordResetForm()
    
    return render(request, 'myauth/confirm_password_reset.html', {'form': form, 'title': 'Confirm Password Reset'})

@login_required
def change_password_view(request):
    """Change the user's password."""
    print(request.user)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            logger.info("Changing password for user: %s", request.user.username)
            user = request.user
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()

            messages.success(request, 'Your password has been changed successfully.')
            login(request, authenticate(username=user.username, password=new_password))
            return redirect('note_list')
    else:
        form = ChangePasswordForm()
    
    return render(request, 'myauth/change_password.html', {'form': form, 'title': 'Change Password'})


"""HELPER FUNCTIONS"""

def is_expired(datetime):
    """Check if the given datetime is 10 minutes in the past."""
    return datetime < timezone.now() - timezone.timedelta(minutes=10)
