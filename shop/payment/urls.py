from django.urls import path
from . import views

urlpatterns = [
    path('cards/', views.CardManager.as_view(), name="card manager"),
    # path('cart', views.AddRemoveToCart.as_view(), name='add remove cardt'),
]