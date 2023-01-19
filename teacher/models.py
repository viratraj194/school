from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification

class Teacher(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='user_profile', on_delete=models.CASCADE)
    teacher_name = models.CharField(max_length=50, )
    teacher_file = models.ImageField(upload_to='teacher/file')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.teacher_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # update
            orig = Teacher.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved
                }

                if self.is_approved == True:
                    # send notification email
                    mail_subjects = 'congratulation! your restaurant is approved'
                    mail_template = 'accounts/emails/admin_approval_email.html'

                    send_notification(mail_subjects, mail_template, context)
            else:
                # send notification email
                mail_subjects = 'sorry your are not eligible for publishing your food manu in public marketplace'
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved
                }
                send_notification(mail_subjects, mail_template, context)
        return super(Teacher, self).save(*args, **kwargs)
