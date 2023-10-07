from django.urls import path
from . import views
urlpatterns = [
    path('home/', views.t),
    path('sinup/', views.RegisterUser.as_view(), name="register"),
]