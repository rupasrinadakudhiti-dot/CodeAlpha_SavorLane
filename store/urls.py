from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
urlpatterns=[
 path('',views.home,name='home'), path('products/',views.product_list,name='products'), path('products/<slug:slug>/',views.product_detail,name='product_detail'),
 path('register/',views.register_view,name='register'), path('login/',auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'), path('logout/',auth_views.LogoutView.as_view(),name='logout'),
 path('cart/',views.cart_detail,name='cart'), path('cart/add/<int:product_id>/',views.cart_add,name='cart_add'), path('cart/update/<int:product_id>/',views.cart_update,name='cart_update'), path('cart/remove/<int:product_id>/',views.cart_remove,name='cart_remove'),
 path('checkout/',views.checkout,name='checkout'), path('orders/',views.order_history,name='orders'), path('orders/<int:order_id>/success/',views.order_success,name='order_success')]
