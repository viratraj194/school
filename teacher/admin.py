from django.contrib import admin
from .models import Teacher

class TeacherAdmin(admin.ModelAdmin):
    list_filter = ('user', 'teacher_name')
    list_display = ('user', 'teacher_name', 'created_date', 'modified_at', 'is_approved')


admin.site.register(Teacher, TeacherAdmin)
