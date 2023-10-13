from django.urls import path
from . import views
urlpatterns = [
    path('add/', views.SopeCreateView.as_view(), name="add shop"),
    path('edite/<str:username>/', views.ShopEditeView.as_view(), name="edite shop"),
    path('delete/<str:username>/', views.ShopDeleteView.as_view(), name="delete shop"),
    path('manager', views.ShopManagerView.as_view(), name="shop manager"),
    path('managment/<str:username>/', views.ShopMnagementView.as_view(), name="management"),
    path('managment/<str:username>/products/', views.ShopAddListProductView.as_view(), name="add product"),
    path('managment/<str:username>/delete/<int:pk>/', views.DeleteProduct.as_view(), name='delete product'),
]