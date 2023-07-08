from django.db import models

from django.shortcuts import render
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps
from django.utils.html import mark_safe
from django.contrib.postgres.fields import ArrayField

from users.models import User


# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser
# python manage.py runserver
# pip install psycopg2


class Category(models.Model):

    class Meta:

        db_table = "category"

    name = models.CharField(max_length=100)

    description = models.CharField(max_length=100)

    def __str__(self):

        return self.name


class Product(models.Model):

    class Meta:

        db_table = "products"

    name = models.CharField(max_length=100)

    description = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    photo_0 = models.ImageField(upload_to="photos/%Y/%m/%d/", null=False)
    photo_1 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    photo_2 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    photo_3 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)

    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" height="100px" />'%(self.photo_0.url))
    image_tag.short_description = 'Image'


    category = models.ForeignKey(Category, on_delete=models.RESTRICT)


def __str__(self):

    return f"{self.name} {self.description} {self.price} {self.catedory}"


@receiver(post_migrate)
def populate_data(sender, **kwargs):
    if sender.name == 'shop':
        Category = apps.get_model('shop', 'Category')
        Product = apps.get_model('shop', 'Product')
        categories = [
            {'name': 'Category 1', 'description': 'Description 1'},
            {'name': 'Category 2', 'description': 'Description 2'},
            {'name': 'Category 3', 'description': 'Description 3'},
        ]
        for category_data in categories:
            category = Category(
                name=category_data['name'], description=category_data['description'])
            category.save()
        category_objects = Category.objects.all()
        products = [
            {'name': 'Product 1', 'description': 'Description 1',
                'price': 10.0, 'category': category_objects[0]},
            {'name': 'Product 2', 'description': 'Description 2',
                'price': 20.0, 'category': category_objects[1]},
            {'name': 'Product 3', 'description': 'Description 3',
                'price': 30.0, 'category': category_objects[2]},
        ]

        for product_data in products:

            product = Product(

                name=product_data['name'],

                description=product_data['description'],

                price=product_data['price'],

                category=product_data['category']

            )

            product.save()

        
class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True) #takes time NOW

    def __str__(self):
        return f'Basket for {self.user.username} | Product: {self.product.name}'
    
    def sum(self):
        return self.product.price * self.quantity

    def get_json(self):
        item={
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum())
        }
        return item
   
    
    @classmethod
    def create_or_update(cls, product_id, user):
        baskets = Basket.objects.filter(user=user, product_id=product_id)
            
        if not baskets.exists():
            obj = Basket.objects.create(user=user, product_id=product_id, quantity=1)
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
            is_created = False
            return basket, is_created


class DeliveryDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    address_line_1 = models.CharField(null=False, blank=False)
    address_line_2 = models.CharField(null=True, blank=True)
    country = models.CharField(null=False, blank=False)
    city = models.CharField(null=False, blank=False)
    state = models.CharField(null=False, blank=False)
    zip_code = models.CharField(null=True, blank=True)

    @classmethod
    def create_delivery_details(cls, user, address_line_1, address_line_2, country, city, state, zip_code):
        DeliveryDetails.objects.create(user=user, address_line_1=address_line_1, address_line_2=address_line_2, country=country, city=city, state=state, zip_code=zip_code)

class Order(models.Model):
    order_number = models.CharField(null=False)
    products_in_basket = ArrayField(ArrayField(models.CharField(null=False, blank=False)))
    delivery_details = models.ForeignKey(DeliveryDetails, on_delete=models.CASCADE, blank=True, null=True)
    total = models.FloatField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    
    @classmethod
    def create_order(cls,order_number, products_in_basket, delivery_details, total, user):
        Order.objects.create(order_number=order_number, products_in_basket=products_in_basket, delivery_details=delivery_details, total=total, user=user)
       
    def get_json(self):
        item={
            'order_number': self.order_number,
            'products_in_basket': self.products_in_basket,
            'address_line_1': self.delivery_details.address_line_1,
            'address_line_2': self.delivery_details.address_line_2,
            'country': self.delivery_details.country,
            'city': self.delivery_details.city,
            'state': self.delivery_details.state,
            'zip_code': self.delivery_details.zip_code,
            'total': self.total,
            'user': self.user,
        }
        return item


class ContactRequest(models.Model):
    name=models.CharField(null=False, blank=False)
    email=models.CharField(null=False, blank=False)
    subject=models.CharField(null=True, blank=True)
    message=models.CharField(null=False, blank=False)

    def get_json(self):
        item={
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
        }
        return item

    @classmethod
    def create_request(cls,name, email, subject, message):
        ContactRequest.objects.create(name=name, email=email, subject=subject, message=message)


class RecentlyViewedProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)

    @classmethod
    def create(cls,user, product):
        RecentlyViewedProducts.objects.create(user=user, product=product)