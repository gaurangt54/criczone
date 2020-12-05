from . import views
from django.urls import path


urlpatterns = [

    path('login/', views.loginPage, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/', views.userPage, name='user-page'),

    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),

    path('create_product/', views.createProduct, name='create_product'),
    path('update_product/<str:pk>/', views.updateProduct, name='update_product'),
    path('delete_product/<str:pk>/', views.deleteProduct, name='delete_product'),

    path('category/<str:pk>/', views.category, name='category'),


    path('products/', views.products, name='products'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('account/', views.accountSettings, name='account'),

    path('add_cart/<str:pk>/', views.addCart, name='add_cart'),
    path('view_cart/', views.viewCart, name='view_cart'),
    path('delete_cart/<str:pk>/', views.deleteCart, name='delete_cart'),

    path('checkout/', views.checkout, name='checkout'),

    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),


]
