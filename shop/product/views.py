from functools import wraps
from django.shortcuts import render

from .models import Product, Category
from users.models import User

def context_data(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        products = Product.objects.order_by('name')
        categories = Category.objects.order_by('name')
        user = User.objects.filter(username=request.user.username) 
        print("USER => ", user)
        context = {
            "products": products,
            'categories': categories,
            'users': user

        }
        return func(request, *args, context=context, **kwargs)
    return wrapper

@context_data
def index(request, context):
    user = User
    print("user", user.username)
    return render(request, 'pages/index.html', context)
    
@context_data
def shop(request, context):

    query = request.GET.get('category')
    print("Query => ", query)

    if query == None:
        products = Product.objects.order_by('name')
    else:
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

    categories = Category.objects.order_by('name')
    user = User.objects.order_by('username')
    print("USER => ", user)

    context = {
        "products" : products,
        "categories" : categories,
        "users" : user
    }
    return render(request, 'pages/shop.html', context)

@context_data
def cart(request):
    return render(request, 'pages/cart.html')

@context_data
def checkout(request, context):
    return render(request, 'pages/checkout.html')

@context_data
def contact(request, context):
    return render(request, 'pages/contact.html', context)

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
    context = {
        "detailed_product" : detailed_product,
        "products" : products,
    } 

    return render(request, 'pages/detail.html', context)


