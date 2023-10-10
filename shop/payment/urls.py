from django.urls import path
from . import views

urlpatterns = [
    path('cards/', views.CardManager.as_view(), name="card manager"),
    path('request-payment/', views.RequestPaymentView.as_view(), name="request payment"),
]