from django.urls import path
from . import views
urlpatterns = [
    path('add/', views.SopeCreateView.as_view(), name="add shop"),
    path('edite/<str:username>/', views.ShopEditeView.as_view(), name="edite shop"),
    path('delete/<str:username>/', views.ShopDeleteView.as_view(), name="delete shop"),
    
]