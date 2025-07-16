from django.db import models
from django.contrib.auth.models import User
import datetime

class Category(models.Model):
    name = models.CharField(max_length=50,null=False,blank=False)
    image = models.ImageField(upload_to="media/images",default='image',null=True,blank=True)
    details = models.TextField(max_length=5000,default="")
    status = models.BooleanField(default=False,help_text='0=default,1=Hidden')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Category'

class Brand(models.Model):
    category = models.ForeignKey(to='Category', on_delete = models.CASCADE)
    name = models.CharField(max_length=50,null=False,blank=False)
    image = models.ImageField(upload_to="media/images",default='image',null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Brand'

class Product(models.Model):
    category = models.ForeignKey(to='Category', on_delete = models.CASCADE)
    name = models.CharField(max_length=50,null=False,blank=False)
    image = models.ImageField(upload_to="media/images",default='image',null=True,blank=True)
    about = models.TextField(max_length=3000,null=False,blank=False)
    details = models.TextField(max_length=5000,default="")
    original_price  = models.FloatField(default=0,null=True,blank=True)
    selling_price  = models.FloatField(default=0,null=True,blank=True)
    quantity  = models.IntegerField(default=0,null=True,blank=True)
    mfdate = models.DateField() 
    expiry = models.DateField() 
    status = models.BooleanField(default=False, help_text='0=default,1=Hidden')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Product'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(to='Product', on_delete = models.CASCADE)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    price = models.FloatField(default=0,null=True,blank=True)

    def __str__(self):
        return self.product

    class Meta:
        db_table = 'Cart'

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)

    def __str__(self):
        return self.product

    class Meta:
        db_table = 'Wishlist'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    fname = models.CharField(max_length=50,null=False,blank=False)
    lname = models.CharField(max_length=50,null=False,blank=False)
    email = models.CharField(max_length=50,null=False,blank=False)
    phone = models.CharField(max_length=50,null=False,blank=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=50,null=False,blank=False)
    state = models.CharField(max_length=50,null=False,blank=False)
    country = models.CharField(max_length=50,null=False,blank=False)
    zipcode = models.CharField(max_length=50,null=False,blank=False)
    total = models.CharField(max_length=50,null=False,blank=False)
    paymentmode = models.CharField(max_length=150,null=False,blank=False)
    paymentid = models.CharField(max_length=150,null=True)
    orderstatus = (('Placed','Placed'),('Shipped','Shipped'),('Delivered','Delivered'))
    status = models.CharField(max_length=50,choices=orderstatus,default='Placed')
    message = models.TextField(null=True)
    trackingid = models.CharField(max_length=500,null=True)
    created_on = models.DateTimeField(default=datetime.datetime.now())
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}-{}'.format(self.id,self.trackingid)

    class Meta:
        db_table = 'Order'

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField(default=0,null=False,blank=False)
    price = models.FloatField(default=0,null=False,blank=False)
    subtotal = models.FloatField(default=0,null=False,blank=False)
    
    def __str__(self):
        return '{}-{}'.format(self.order.id,self.order.trackingid)

    class Meta:
        db_table = 'OrderItems'

class Account(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    phone = models.CharField(max_length=50,null=False,blank=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=50,null=False,blank=False)
    state = models.CharField(max_length=50,null=False,blank=False)
    country = models.CharField(max_length=50,null=False,blank=False)
    zipcode = models.CharField(max_length=50,null=False,blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Account'


