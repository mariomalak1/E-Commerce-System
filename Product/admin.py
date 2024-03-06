from django.contrib import admin
from .models import Brand, Category, SubCategory, Product, Productmages
# Register your models here.

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(Productmages)