from django.urls import path
from . import views
urlpatterns = [
    path('add/', views.SopeCreateView.as_view(), name="add shop"),
    path('edite/<str:username>/', views.ShopEditeView.as_view(), name="edite shop"),
    path('delete/<str:username>/', views.ShopDeleteView.as_view(), name="delete shop"),
    path('manager', views.ShopManagerView.as_view(), name="shop manager"),
    path('managment/<str:username>/', views.ShopMnagementView.as_view(), name="management"),
    path('managment/<str:username>/products/', views.ShopAddListProductView.as_view(), name="add product"),
    path('managment/<str:username>/delete/<int:pk>/', views.DeleteProductView.as_view(), name='delete product'),
    path('managment/<str:username>/details/<int:pk>', views.DetailsProductView.as_view(), name='details product'),
    path('managment/<str:username>/categorys/', views.CategoryManagerView.as_view(), name="categorys manager"),
    path('managment/<str:username>/categorys/delete/<int:pk>', views.DeleteCategoryView.as_view(), name="delete category"),
    path('managment/<str:username>/categorys/edite/<int:pk>/', views.EditeCategoryView.as_view(), name="edite category"),
    path('managment/<str:username>/orderproducts/', views.OrderListView.as_view(), name='orders product'),
    path('managment/<str:username>/info-sells', views.InfoSellView.as_view(), name='info sells'),
    path('managment/<str:username>/request-payment/', views.RequestPaymentView.as_view(), name="request payment"),
]