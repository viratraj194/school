from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode

from .forms import UserForm
from teacher.forms import TeacherForm
from .models import User, UserProfile
from django.contrib import messages, auth
from . utils import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from .utils import send_verification_email

def home(request):
    return render(request, 'accounts/home.html')


def registerUser(request):
    if request.method == 'POST':
        # print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.STUDENT
            user.save()
            mail_subject = 'activate your account'.title()
            mail_template = 'accounts/emails/send_verification_email.html'
            send_verification_email(request, user, mail_subject, mail_template)
            messages.success(request, 'successfully! you have registered, please wait for the approval'.title())
            return redirect('home')
        else:
            print(form.errors)
    else:

        form = UserForm
    context = {
        'form': form
    }

    return render(request, 'accounts/registerUser.html', context)


def registerTeacher(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        t_form = TeacherForm(request.POST, request.FILES)
        if form.is_valid() and t_form.is_valid():
            fist_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=fist_name, last_name=last_name, username=username, email=email,
                                            password=password)
            user.role = User.TEACHER
            user.save()
            teacher = t_form.save(commit=False)
            teacher.user = user
            user_profile = UserProfile.objects.get(user=user)
            teacher.user_profile = user_profile
            teacher.save()
            #send_verification_email()
            mail_subject = 'activate your account'.title()
            mail_template = 'accounts/emails/send_verification_email.html'
            send_verification_email(request, user, mail_subject, mail_template)
            messages.success(request, 'your registration was successful! please wait for approval')
            return redirect('registerTeacher')
        else:
            print('error')
            print(form.errors)

    else:
        form = UserForm
        t_form = TeacherForm
    context = {
        'form': form,
        't_form': t_form
    }

    return render(request, 'accounts/registerTeacher.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'your account is activated'.title())

        return redirect('account')
    else:
        messages.error(request, 'invalid activation link'.title())
        return redirect('account')



def login(request):
    if request.method == 'POST':
        # print(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you have successfully logged in '.title())
            # print('success')
            return redirect('account')
        else:
            messages.error(request, 'error')
            return redirect('login')
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.success(request, 'you logged out successfully'.title())
    return redirect('login')

@login_required(login_url='login')
def account(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect( redirectUrl)

def check_user_role_for_student(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def check_user_role_for_teacher(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

@login_required(login_url='login')
@user_passes_test(check_user_role_for_student)
def studentAccount(request):
    return render(request, 'accounts/studentAccount.html')


@login_required(login_url='login')
@user_passes_test(check_user_role_for_teacher)
def teacherAccount(request):
    return render(request, 'accounts/teacherAccount.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            #send email to reset password
            mail_subject = 'please click the link to reset the password'.title()
            mail_template = 'accounts/emails/reset_password.html'
            send_verification_email(request, user, mail_subject, mail_template)
            messages.success(request, 'the password reset mail sent to email '.title())
            return redirect('login')

        else:
            messages.error(request, "email didn't exists".title())
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk =uid )
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.info(request, 'please reset the password'.title())
        return redirect('reset_password')
    else:
        messages.error(request, 'this link is expired ')
        return redirect('account')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        conform_password = request.POST['conform_password']
        if password == conform_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request,'password reset is successful'.title())
            return redirect('login')
        else:
            messages.error(request, 'password did not match'.title())
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')




