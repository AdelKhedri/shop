from django.urls import path
from . import views
urlpatterns = [
    path('sinup/', views.RegisterUser.as_view(), name="register"),
    path('sinup/confirm_phone/', views.RegisterPhone.as_view(), name="register phone"),
    path('sinin/', views.SininUser.as_view(), name="sinin"),
    path('forget_password/', views.ForgetPasswordView.as_view(), name='forget password'),
    path('forget_password/confirm/', views.ConfirmForgetPasswordView.as_view(), name='confirm forget password'),
    path('change_password/', views.ChangePassword.as_view(), name="change password"),
    path('notifacations', views.NotifacationView.as_view(), name="notifacations"),
    path('', views.ProfileUpdate.as_view(), name="update profile"),
    path('support/', views.SupportView.as_view(), name='support'),
    path('logout', views.logout_view, name='logout'),
]