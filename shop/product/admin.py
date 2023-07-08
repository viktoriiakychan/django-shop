from django.contrib import admin

from .models import Category, ContactRequest, Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'image_tag')
    list_display_links = ('id', 'name') #clickable
    list_editable = ('price',)
    list_per_page = 30
    search_fields = ('name', 'price', 'description')
    list_filter = ('name', )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name') #clickable
    list_editable = ('description')
    list_per_page = 30

class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message')
    list_display_links = ('name', 'message') #clickable
    list_per_page = 10
    search_fields = ('name', 'subject', 'email')

    
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ContactRequest, ContactRequestAdmin)