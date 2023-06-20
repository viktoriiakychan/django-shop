from django.shortcuts import render

from .models import Product, Category




def index(request):
    products = Product.objects.order_by('name')
    categories = Category.objects.order_by('name')
    context = {
        "products" : products,
        "categories" : categories
    }
    return render(request, 'pages/index.html', context)


def shop(request):

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

    context = {
        "products" : products,
        "categories" : categories
    }
    return render(request, 'pages/shop.html', context)

def cart(request):
    return render(request, 'pages/cart.html')

def checkout(request):
    return render(request, 'pages/checkout.html')

def contact(request):
    return render(request, 'pages/contact.html')

def detail(request):
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

def login(request):
    query = request.GET
    print("QUERY => ", query)

    return render(request, 'authorisation/login.html')

def log_in(request):
    query = request.GET
    print("QUERY => ", query)