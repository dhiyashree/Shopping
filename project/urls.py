from django.urls import path
from .import views
from .views import product_list, product_detail, checkout, order_success,next_page

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('checkout/', checkout, name='checkout'),
    path('order_success/<int:order_id>/', order_success, name='order_success'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('buy_now/<int:product_id>/',views.buy_now, name='buy_now'),
    path('order_confirmation/<int:order_id>/',views.order_confirmation,name='order_confirmation'),
    
    path('next_page/',views.next_page,name='next_page'),

    path('cart/', views.cart_view, name='cart'),




    path('pay/', views.initiate_payment, name='initiate_payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    
    
]

