from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order,Shipping
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.contrib.auth.models import User,auth
from .models import Cart
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .services.razorpay_services import create_order,verify_payment
from .models import*


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        quantity = request.POST.get('quantity')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')

        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            address=address,
            phone_number=phone_number
        )
        
        # Create shipping entry
        shipping = Shipping.objects.create(order=order, tracking_number="TRK123456")
        
        return redirect('order_success', order_id=order.id)  # Redirect to order success page
    return render(request, 'product_detail.html', {'product': product})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})


#payment integrate
# stripe.api_key = settings.STRIPE_SECRET_KEY  

@login_required
def checkout(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        
        # Create a charge
        charge = stripe.Charge.create(
            amount=int(order.product.price * 100),  # Amount in cents
            currency='usd',
            description=f'Order {order.id}',
            source=request.POST['stripeToken']
        )

        order.status = 'Paid'
        order.save()

        return redirect('order_success', order_id=order.id)
    return render(request, 'checkout.html')

def next_page(request):
    return render(request,'next_page.html')




def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return render(request,'cart.html')


def cart_view(request):
    cart_items = Cart.objects.all()
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})



def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        order = Order.objects.create(product=product)
        amount = int(product.price)  # Get amount from form or request
        order = create_order(amount)
        context = {
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'order_id': order['id'],
            'amount': amount * 100,  # Amount in paise for Razorpay
            'currency': order['currency'],
        }
        return render(request, 'checkout.html', context)
        # Add logic for payment processing here

    return render(request, 'buy_now.html', {'product': product})    


def order_confirmation(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    return render(request,'order_confirmation.html',{'order':order})


def remove_from_cart(request, product_id):
    cart_item = Cart.objects.get(product_id=product_id)
    cart_item.delete()
    return redirect('cart')

    
def initiate_payment(request):
    if request.method == "POST":
        amount = int(request.POST['amount'])  # Get amount from form or request
        order = create_order(amount)
        context = {
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'order_id': order['id'],
            'amount': amount * 100,  # Amount in paise for Razorpay
            'currency': order['currency'],
        }
        return render(request, 'payments/checkout.html', context)
    return render(request, 'payments/pay.html')

@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        # Verify the payment
        if verify_payment(payment_id, order_id, signature):
            # save to database
            Payment.objects.create(
                payment_id=payment_id,
                order_id=order_id,
                amount=1000,  # You can store actual amount from order
                status='Success'
            )
            return render(request,'success.html')

        else:
            # Payment failed
            Pay.objects.create(
                payment_id=payment_id,
                order_id=order_id,
                amount=1000,
                status='Failed'
            )
            return render(request, 'payments/failure.html')
    return redirect('initiate_payment')
  


