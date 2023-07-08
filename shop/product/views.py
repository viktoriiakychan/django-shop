from email.message import EmailMessage
from functools import wraps
import smtplib
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from prettytable import PrettyTable

from product.forms import ProductPlaceOrderForm, ContactForm
from .models import Basket, ContactRequest, DeliveryDetails, Order, Product, Category, RecentlyViewedProducts
from users.models import User
from django.views.generic import CreateView, View, TemplateView
from django.contrib.auth.tokens import default_token_generator
from django.utils.crypto import get_random_string
from django.db.models import Q

def context_data(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        products = Product.objects.order_by('name')
        categories = Category.objects.order_by('name')
        # user = User.objects.filter(username=request.user.username),
        user = User.objects.order_by('username')
        print("USERS ==> ", user)
        paginator = Paginator(products, 2)
        print(f"paginator {paginator}")
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        
        quantity = 0

        context = {
            "products": page,
            'categories': categories,
            'users': user,
            'quantity': quantity,
        }
        return func(request, *args, context=context, **kwargs)
    return wrapper

@context_data
def index(request, context):
    if request.user.is_authenticated:
        basket_quantity = 0
        items_in_basket = Basket.objects.filter(user=request.user)
        for basket in items_in_basket:
            basket_quantity += basket.quantity

        context["quantity"] = basket_quantity
        context["recent_products"] = RecentlyViewedProducts.objects.order_by('product')

    return render(request, 'pages/index.html', context)

@context_data
def shop(request, context):
    query = request.GET.get('category')
    print("Query => ", query)
    if query:
        sorted_products = []
        print ("== not none!")
        products = Product.objects.order_by('name')
        for product in products:
            if str(product.category) == str(query):
                print("equal")
                sorted_products.append(product)
            else:
                print("not equal")
        print(sorted_products)
        products = sorted_products
    else:
        products = Product.objects.order_by('name')

    search_query = request.GET.get('search')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(category__name__icontains=search_query))
    elif min_price or max_price:
        if min_price and max_price:
            print('GOOOOD')
        else:
            if not min_price: min_price = 0
            else: max_price = float('inf')
        print("MIN => ", min_price)
        print("MAX => ", max_price)
        
        products = products.filter(price__gte=min_price, price__lte=max_price)

    categories = Category.objects.order_by('name')
    user = User.objects.order_by('username')
    print("USER => ", user)
    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    quantity = 0
    items_in_basket = Basket.objects.filter(user=request.user)

    for basket in items_in_basket:
        quantity += basket.quantity

    context = {
        "products" : page,
        "categories" : categories,
        "users" : user,
        'quantity': quantity,
        'search_query': search_query,
    }
    return render(request, 'pages/shop.html', context)

@context_data
def cart(request, context):
    items_in_basket = Basket.objects.filter(user=request.user)
    total = 0
    quantity = 0

    for basket in items_in_basket:
        total += basket.sum()
        quantity += basket.quantity

    print("BASKET => ", quantity)
    user = User.objects.order_by('username')
    print("USER => ", user)

    context = {
        'total': total,
        'basket': items_in_basket,
        'quantity': quantity,
        'users': user
    }
    return render(request, 'pages/cart.html', context)

@context_data
def checkout(request, context):
    items_in_basket = Basket.objects.filter(user=request.user)
    total = 0
    basket_quantity = 0

    for basket in items_in_basket:
        total += basket.sum()
        basket_quantity += basket.quantity

    context['total'] = total
    context['quantity'] = basket_quantity

    return render(request, 'pages/checkout.html', context)

@context_data
def contact(request, context):
    if request.user.is_authenticated:
        basket_quantity = 0
        items_in_basket = Basket.objects.filter(user=request.user)
        for basket in items_in_basket:
            basket_quantity += basket.quantity
    
        context["quantity"] = basket_quantity
        
    return render(request, 'pages/contact.html', context)

@login_required
@context_data
def detail(request, context):
    query = request.GET.get('product')
    print("Query => ", query)

    products = Product.objects.order_by('name')

    if query == None:
        print("404 ERROR")
    else:
        detailed_product = None
        products = Product.objects.order_by('name')
        for product in products:
            if str(product.name) == str(query):
                print("equal")
                detailed_product = product
            else:
                print("not equal")
    print("Photo => ", detailed_product.photo_0)
    print("Photo => ", detailed_product.photo_1)

    basket_quantity = 0
    items_in_basket = Basket.objects.filter(user=request.user)
    for basket in items_in_basket:
        basket_quantity += basket.quantity
    
    context["detailed_product"] = detailed_product
    context["products"] = products
    context["quantity"] = basket_quantity

    if not RecentlyViewedProducts.objects.filter(user=request.user, product=detailed_product).count() > 0:
        RecentlyViewedProducts.create(request.user, detailed_product)

    return render(request, 'pages/detail.html', context)

@login_required
@context_data
def add_to_cart(request, product_id, context):
    if not request.user.is_authenticated:
        return render(request, 'pages/index.html', context)
    Basket.create_or_update(product_id, request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def remove_from_cart(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
@context_data
def place_order(request, context):
        user = request.user
        
        if request.method == 'POST': #if everything is submitted 
            form = ProductPlaceOrderForm(request.POST)
            if form.is_valid():
                order_number = get_random_string(length=15)
                products_in_basket = Basket.objects.filter(user=user)
                total = 0
                order_total = 0
                products_in_basket_names = []
                
                order_details = PrettyTable(['Qty', 'Item', 'Price', 'Total'])
                for item in products_in_basket:
                    total = 0
                    total += item.sum()
                    order_total += total
                    order_details.add_row([item.quantity, item.product.name, item.product.price, total])
                    products_in_basket_names.append(item.product.name)
                if not DeliveryDetails.objects.filter(address_line_1 = form.cleaned_data['address_line_1'], address_line_2 = form.cleaned_data['address_line_2'], user=user).count() > 0:
                #     print('already exists !!!!!!!!!!!!!!!!!!!!')
                # else:
                    DeliveryDetails.create_delivery_details(user, form.cleaned_data['address_line_1'], form.cleaned_data['address_line_2'], form.cleaned_data['country'], form.cleaned_data['city'], form.cleaned_data['state'], form.cleaned_data['zip_code'])

                Order.create_order(order_number, products_in_basket_names, DeliveryDetails.objects.filter(address_line_1 = form.cleaned_data['address_line_1'], address_line_2 = form.cleaned_data['address_line_2'],user=user).first(), order_total,user)

                from_email = 'Order confirmation <confirmationofregistration@ukr.net>'
                to_email = [user.email]
                current_order = Order.objects.filter(order_number=order_number).first()
                message_body = f"Hiya, {user.first_name}!\nHere is the confirmation of yout order.\n\n\nOrder Details\n\n{order_details}\nDelivery Details\n\nOrder number: {current_order.get_json()['order_number']}\n\nDelivery Address: {current_order.get_json()['address_line_1']}, {current_order.get_json()['address_line_2']}, {current_order.get_json()['city']}, {current_order.get_json()['state']}, {current_order.get_json()['country']}, {current_order.get_json()['zip_code']}"
                
                print("MESSAGE ===> ", message_body)
                msg = EmailMessage()
                msg['From'] = from_email
                msg['To'] = to_email
                msg['Subject'] = f'Thanks for your order, {user.first_name}!'
                msg.set_content(message_body)
                
                user.is_active = True
                user.save()


                server = smtplib.SMTP_SSL('smtp.ukr.net', 2525)
                server.login("confirmationofregistration@ukr.net", "RxFucyKX5nqimoOk")
                server.send_message(msg)

                server.quit()

                #DELETE FROM THE BASKET
                Basket.objects.filter(user=user).delete()

                context["form"] = form
                context["users"] = user
                
                # POSSIBLY A PAGE WITH "YOUR ORDER HAS BEEN PLACED" (nstead of index)
                return render(request, 'pages/index.html')
        else:
            form = ProductPlaceOrderForm()
            # POSSIBLY A PAGE WITH "SOMETHING WENT WRONG" (nstead of index)

        return render(request, 'pages/index.html', context)

@login_required
def increase_quantity(request, basket_id):
        basket = Basket.objects.get(id=basket_id)
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def decrease_quantity(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.quantity -= 1
    if basket.quantity == 0:
        basket.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        basket.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


@context_data
def contact_admin(request, context):
    if request.method == 'POST': #if everything is submitted 
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            ContactRequest.create_request(name,email,subject,message)

            from_email = 'MultiShop Team <confirmationofregistration@ukr.net>'
            to_email = [email]
            message_body = f"Hello, {name}!\n\nThank you very much for contacting us! We do appreciate it.\nWe'll try to get you back to you with your query as soon as possible!\n\nThanks a mill,\nYour lovely MultiShop Team"
                
            print("MESSAGE ===> ", message_body)
            msg = EmailMessage()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = f'Thanks for getting in touch with us, {name}!'
            msg.set_content(message_body)

            user = request.user
            if user and user.is_authenticated:
                user.is_active = True
                user.save()

            server = smtplib.SMTP_SSL('smtp.ukr.net', 2525)
            server.login("confirmationofregistration@ukr.net", "RxFucyKX5nqimoOk")
            server.send_message(msg)

            server.quit()        
           
    return render(request, 'pages/index.html', context)
               

