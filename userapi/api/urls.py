from django.urls import path
from userapi.api.views import (UserSignUpView,UserLoginView,ForgotPasswordView,TeacherAddStudentView,
StudentListView,StudentDetailView,AdminAddUserView,UserListView)



urlpatterns = [
    path('signup',UserSignUpView.as_view(),name='signup_user'),
    path('login',UserLoginView.as_view(),name='login'),
    path('forgot/password',ForgotPasswordView.as_view(),name='change-password'),
    path('teacher/create',TeacherAddStudentView.as_view(),name='teacher-add-student'),
    path('teacher/list',StudentListView.as_view(),name='student-list'),
    path('student/detail',StudentDetailView.as_view(),name='student-detail'),
    path('admin/add',AdminAddUserView.as_view(),name='admin-add-user'),
    path('users',UserListView.as_view(),name='users-list')

]