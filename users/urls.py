from django.urls import path
from .views import (RegisterView,LoginView,
                    ForgetPasswordView, ResetPasswordView,
                    ContactListView, ContactDetailView)

urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    path('forget-password/', ForgetPasswordView.as_view(), name='forget password'),
    path('reset-password/<str:token>/', ResetPasswordView.as_view(), name='reset password'),

    path('contacts/', ContactListView.as_view(), name='contact list'),
    path('contacts/<pk>/', ContactDetailView.as_view(), name='contact detail')

]