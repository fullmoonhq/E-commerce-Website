from django.contrib import admin
from .models import Category,Product,Cart,Wishlist,Order,OrderItems,Account,Brand
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(Account)
admin.site.register(Brand)