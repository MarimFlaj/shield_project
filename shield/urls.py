from django.urls import path

from .views import *
from django.contrib.auth.views import LogoutView


app_name = 'shield'

urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('login/', LoginView.as_view(template_name='login_register.html',next_page='/'), name='login'),
    # path('login/', auth_views.LoginView.as_view(template_name='login_register.html',next_page='/'), name='login'),

    path('register', RegisterView.as_view(), name='register'),

    path('', SystemOverView.as_view(), name='home'),
    path('urls', UrlView.as_view(), name='urls'),
    path('users', UserView.as_view(), name='users'),
    path('TrainingPackage', TrainingPackageView.as_view(), name='TrainingPackage'),
    path('Departments', DepartmentsView.as_view(), name='Departments'),
    path('SendingURls', SendingURlsView.as_view(), name='SendingURls'),
    path('SendingTraining', SendingTrainingView.as_view(), name='SendingTraining'),

    path('urljson', UrlJson.as_view(), name='urljson'),
    path('usersjson', UsersJson.as_view(), name='usersjson'),
    path('TrainingPackageJson', TrainingPackageJson.as_view(), name='TrainingPackageJson'),
    path('DepartmentJson', DepartmentJson.as_view(), name='DepartmentJson'),
    path('SendingURlsJson', SendingURlsJson.as_view(), name='SendingURlsJson'),
    path('SendingTrainingJson', SendingTrainingJson.as_view(), name='SendingTrainingJson'),

    path('ReportView', ReportView.as_view(), name='ReportView'),
    path('SystemOverView', SystemOverView.as_view(), name='SystemOverView'),
    path('MyProfile', MyProfile.as_view(), name='MyProfile'),
    path('ForgetPassword', ForgetPassword.as_view(), name='ForgetPassword'),
    
    path('chart_api', chart_api, name='chart_api'),
    ]
