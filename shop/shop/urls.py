"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from product.views import index, shop, contact, contact_admin, detail, checkout, cart, add_to_cart, remove_from_cart, place_order ,increase_quantity, decrease_quantity

app_name = 'products'
urlpatterns = [
     path('', index, name='index'),
    
    path('admin/', admin.site.urls),
   
    path('shop/', shop, name='shop'),
    path('contact/', contact, name='contact'),
    
    path('shop/detail/', detail),
    path('shop/checkout/', checkout),
    path('place_order/', place_order, name='place_order'),

    path('shop/cart/', cart),
    path('increase_quantity/<int:basket_id>/', increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:basket_id>/', decrease_quantity, name='decrease_quantity'),

    path('users/', include('users.urls') , name='users'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),    
    path('remove_from_cart/<int:basket_id>/', remove_from_cart, name='remove_from_cart'),

    path('contact_admin/', contact_admin, name='contact_admin'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)