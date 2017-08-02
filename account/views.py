from .forms import CreationFormUser, UpdateFormUser
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from trasher.settings import DEFAULT_FROM_EMAIL
from django.views.generic import *
from .forms import PasswordResetRequestForm, SetPasswordForm
from django.contrib import messages
from .models import User


def register(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password = request.POST['password']
        if password == password1:
            form = CreationFormUser(request.POST)
            if form.is_valid():
                user = form.save()
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user.set_password(form.cleaned_data['password'])
                user.save()
                new_user = authenticate(email=email, password=password)
                login(request, new_user)
                return render(request, 'home.html')
        else:
            errors = 'Password and Conform Password are not equal'
            return render(request, 'registration/register.html', {'errors': errors})
    context = {}
    return render(request, 'registration/register.html', context)


def profile_update(request):
    user = request.user
    if request.method == 'POST' and user.is_authenticated():
        form = UpdateFormUser(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.esn_number = form.cleaned_data['esn_number']
            user.vin_number = form.cleaned_data['vin_number']
            user.save()
            return render(request, 'checkout.html', {'user': user})
    else:
        return redirect('account:register')


def logout_out(request):
    logout(request)
    return redirect('/')


def login_in(request):
    args = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
        else:
            args['login_error'] = u'Пользователь не найден!'
            return render(request, 'registration/login.html', args)
    else:
        return render(request, 'registration/login.html', args)
    return redirect('/')


class ResetPasswordRequestView(FormView):
    template_name = "registration/forgetpassword.html"  # code for template is given below the view's code
    success_url = '/account/reset_password/'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        """
        This method here validates the if the input is an email address or not. Its return type is boolean, True if the input is a email address or False if its not.
        """
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        """
        A normal post request which takes input from field "email_or_username" (in ResetPasswordRequestForm).
        """
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email"]
            if self.validate_email_address(data) is True:  # uses the method written above
                '''
                If the input is an valid email address, then the following code will lookup for
                users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
                '''
                associated_users = User.objects.filter(email=data)
                if associated_users.exists():
                    for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'your site',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }
                        subject_template_name = 'registration/password_reset_subject.txt'
                        # copied from django/contrib/admin/templates/registration/password_reset_
                        # subject.txt to templates directory
                        email_template_name = 'registration/password_reset_email.html'
                        # copied from django/contrib/admin/templates/registration/password_
                        # reset_email.html to templates directory
                        subject = loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                    result = self.form_valid(form)
                    messages.success(request, 'An email has been sent to ' + data +
                                     ". Please check its inbox to continue reseting password.")
                    return result
                result = self.form_invalid(form)
                messages.error(request, 'No user is associated with this email address')
                return result
            else:
                '''
                If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
                '''
                associated_users = User.objects.filter(username=data)
                if associated_users.exists():
                    for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': 'example.com',  # or your domain
                            'site_name': 'example',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }
                        subject_template_name='registration/password_reset_subject.txt'
                        email_template_name='registration/password_reset_email.html'
                        subject = loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                    result = self.form_valid(form)
                    messages.success(request, 'Email has been sent to ' + data +
                                     "'s email address. Please check its inbox to continue reseting password.")
                    return result
                result = self.form_invalid(form)
                messages.error(request, 'This username does not exist in the system.')
                return result
        messages.error(request, 'Invalid Input', {'form': form})
        return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
    template_name = "registration/new_password_confirm.html"
    success_url = '/account/login/'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        user_model = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = user_model._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(request, 'The reset password link is no longer valid.')
            return self.form_invalid(form)


def account_reg_or_guest(request):
    if request.GET.get('account') == 'register':
        return redirect('account:register')
    elif request.GET.get('account') == 'guest':
        return redirect('cart:cart_checkout')
    else:
        return redirect('cart:cart_checkout')
