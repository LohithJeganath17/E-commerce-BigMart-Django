from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from carts.models import CartItem
from .forms import Orderform
from .models import OrderModel,Payment,OrderProduct
from store.models import ProductModel
import json
import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
# Create your views here.




def payments(request):

    #print("Payments view hit!")

    try:
        if request.method != "POST":
            #print("❌ Not a POST request")
            return JsonResponse({'error': 'Only POST allowed'}, status=405)

        # Try to read body
        try:
            body = json.loads(request.body)
            #print("📦 Payload received:", body)
        except Exception as e:
            #print("❌ Failed to parse body:", e)
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        order_id = body.get("orderID")
        trans_id = body.get("transID")
        payment_method = body.get("payment_method")
        status = body.get("status")

        if not all([order_id, trans_id, payment_method, status]):
            #print("❌ Missing data in payload")
            return JsonResponse({'error': 'Missing payment details'}, status=400)
        
    

    #body = json.loads(request.body)
        try:
            order = OrderModel.objects.get( is_ordered=False, order_number=body['orderID'])
            #print("✅ Order fetched:", order)
        except OrderModel.DoesNotExist:
                #print("❌ Order not found:", order_id)
                return JsonResponse({'error': 'Order not found'}, status=404)


        # Store transaction details inside Payment model
        payment = Payment(
            user = order.user,
            payment_id = body['transID'],
            payment_method = body['payment_method'],
            amount_paid = order.order_total,
            status = body['status'],
        )
        payment.save()

        order.payment = payment
        order.is_ordered = True
        order.save()

        # Moving cart items to Order Product table in admin
        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()


            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variation.set(product_variation)
            orderproduct.save()

            # Reduce the quantity of the sold products
            product = ProductModel.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        # Clear cart
        CartItem.objects.filter(user=request.user).delete()

        # Send order recieved email to customer
        mail_subject = 'Thank you for your order!'

        try:
            ##print("📤 Preparing to send email...")
            ##print("👤 order.user:", order.user)
            ##print("📧 order.email:", order.email)
            message = render_to_string('orders/orders_recieved_email.html', {
                    'user': order.user,
                    'order': order,
                })
            to_email = order.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #print("✅ Email sent successfully!")

        except Exception as e:
            pass
            #print("💥 Email sending failed:", str(e))
        
        data = {
            'order_number': order.order_number,
            'transID': payment.payment_id,
        }
        return JsonResponse(data)

    except Exception as e:
        #print("💥 UNEXPECTED ERROR:", str(e))
        return JsonResponse({'error': 'Failed to save payment', 'details': str(e)}, status=500)

def order_complete(request):

    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = OrderModel.objects.get(order_number = order_number, is_ordered = True)
        ordered_products = OrderProduct.objects.filter(order_id = order.id)

        subtotal = 0

        for eachitem in ordered_products:
            subtotal+= eachitem.product_price * eachitem.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order':order,
            'ordered_products':ordered_products,
            'order_number': order.order_number,
            'trans_ID': payment.payment_id,
            'payment': payment,
            'subtotal' : subtotal
        }
        return render(request,'orders/order_complete.html',context)
    
    except(OrderModel.DoesNotExist,Payment.DoesNotExist):
        return redirect('home')


def placeorder(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user = current_user)
    cart_count = cart_items.count()
    if cart_count<=0:
        return redirect('our_store')
    
    tax=0
    grand_total = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax =(5*total)//100
    grand_total = total + tax
    
    if request.method == 'POST':
        
        form = Orderform(request.POST)

        if form.is_valid():
            # Store all the billing information inside Order table
            data = OrderModel()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") 
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = OrderModel.objects.get(user = current_user,is_ordered = False,order_number = order_number)
            context = {
                'order':order,
                'cart_items' : cart_items,
                'total': total,
                'tax' : tax,
                'grand_total' : grand_total,
            }
            #print("Order placed")
            return render(request,'orders/payments.html',context)
    
    else:
        return redirect('checkout')