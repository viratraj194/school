from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registerUser', views.registerUser, name='registerUser'),
    path('registerTeacher/', views.registerTeacher, name='registerTeacher'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('account/', views.account, name='account'),
    path('studentAccount/', views.studentAccount, name='studentAccount'),
    path('teacherAccount/', views.teacherAccount, name='teacherAccount'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password')
]

