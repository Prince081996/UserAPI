from django.urls import path
from userapi.api.views import UserSignUpView,UserLoginView,UpdateUserPasswordView,TeacherCreateView

urlpatterns = [
    path('signup',UserSignUpView.as_view(),name='signup_user'),
    path('login',UserLoginView.as_view(),name='login'),
    path('change/password',UpdateUserPasswordView.as_view(),name='change-password'),
    path('teacher/create',TeacherCreateView.as_view(),name='teacher-add-student'),
    # path('teacher/list',TeacherListView.as_view(),name='teacher-list'),

]