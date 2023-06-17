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
from django.contrib import admin
from django.urls import path
from product.views import index
from product.views import shop
from product.views import cart, checkout, contact, detail

urlpatterns = [

    path('', index, name='index'),
    
    path('admin/', admin.site.urls),
    path('shop/', shop, name='shop'),
    path('contact/', contact),
    
    path('shop/detail/', detail),
    path('shop/checkout/', checkout),
    path('shop/cart/', cart),
]