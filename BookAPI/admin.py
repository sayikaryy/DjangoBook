from django.contrib import admin
from .models import Category, Book, Customer, Order, OrderItem, Payment

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
