from django.contrib import admin
from .models import Product, Catagories, Customer, Order


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'catagory']
    search_fields = ['name']
    list_filter = ["catagory"]
    sortable_by = ["name", "price"]
    autocomplete_fields = ["catagory"]


class AdminCatagories(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "email", "last_name", "phone", "password"]


# Register your models here.
admin.site.register(Product, AdminProduct)
admin.site.register(Catagories, AdminCatagories)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order)
