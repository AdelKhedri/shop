from django.urls import path
from . import views
urlpatterns = [
    path('home/', views.t),
    path('sinup/', views.RegisterUser.as_view(), name="register"),
    path('sinup/confirm_phone/', views.RegisterPhone.as_view(), name="register phone"),
    path('sinin/', views.SininUser.as_view(), name="sinin"),
    path('change_password/', views.ChangePassword.as_view(), name="change password"),
    path('notifacations', views.NotifacationView.as_view(), name="notifacations"),
    path('', views.ProfileUpdate.as_view(), name="update profile"),
    path('support/', views.SupportView.as_view(), name='support')
]