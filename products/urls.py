from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/edit/<int:id>/', views.product_edit, name='product_edit'),
    path('products/delete/<int:id>/', views.product_delete, name='product_delete'),
    path('products/detail/<int:id>/', views.product_detail, name='product_detail'),
    path('products/cart/add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('products/load-dummy/', views.load_dummy_data, name='load_dummy_data'),
    path('products/cart/', views.view_cart, name='view_cart'),
    path('products/cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('products/cart/subtract/<int:id>/', views.subtract_from_cart, name='subtract_from_cart'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
