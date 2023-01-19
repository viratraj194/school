from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
def detectUser(user):
    if user.role == 2:
        redirectUrl = 'studentAccount'
        return redirectUrl
    elif user.role == 1:
        redirectUrl = 'teacherAccount'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl

def send_verification_email(request, user, mail_subject, mail_template):
    from_mail = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(mail_template,{
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_mail = user.email
    mail = EmailMessage(mail_subject, message, from_mail, to=[to_mail])
    mail.send()


def send_notification(mail_subject, mail_template, context):
    from_mail = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    to_mail = context['user'].email
    mail = EmailMessage(mail_subject, message, from_mail, to=[to_mail])
    mail.send()
    return