from django.shortcuts import render,redirect
from store.models import Category,Product,Cart,User,Wishlist,Order,OrderItems,Account,Brand
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from math import ceil
from .forms import UserForm
from django.http import JsonResponse,HttpResponseBadRequest,HttpResponse
import json,random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def homepage(request):
    allbrands = []
    catbrands = Brand.objects.values('category', 'id')
    cats = {item['category'] for item in catbrands}
    for cat in cats:
        brands = Brand.objects.filter(category=cat)
        n = len(brands)
        nos = n // 4 + ceil((n / 4) - (n // 4))
        allbrands.append([brands, range(1, nos)])
    return render(request, 'store/homepage.html', {'allbrands':allbrands})

def category(request):
    cats = Category.objects.all()
    return render(request, 'store/category.html', {'cats': cats})

def viewbycategory(request,cname):
    try:
        products = Product.objects.filter(category__name = cname)
        cat = Category.objects.filter(name = cname).first()
        return render(request, 'store/viewbycategory.html', {'products': products,'cat':cat})

    except:
        messages.warning(request,'Category not found')
        return redirect(category)

def viewproduct(request,pid):
    try:
        product = Product.objects.get(id=pid,status=0)
        return render(request, 'store/viewproduct.html', {'product': product})
    except:
        messages.warning(request,'Product not found')
        return redirect(viewbycategory)

def signup(request):
    form = UserForm()
    if(request.method == "POST"):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(userlogin)
            messages.success(request, 'Registered Successfully,Login to continue')
        else:
            messages.error(request, 'Invalid Credentials')
    return render(request, 'store/register.html', {'form':form})

def userlogin(request):
    if(request.user.is_authenticated):
        messages.warning(request, 'You are already logged in')

    else:

        if(request.method == "POST"):
            uname = request.POST["uname"]
            password = request.POST["pwd"]
            user = authenticate(request,username=uname,password=password)
            
            if user is not None:
                login(request,user)  
                return redirect(homepage)
                messages.success(request, 'Logged in successfully')
            else:
                return redirect(userlogin)
                messages.error(request, 'Invalid Username or Password')

        return render(request, 'store/login.html', {})

def userlogout(request):
    if(request.user.is_authenticated):
        logout(request)
        messages.success(request, 'Logged out successfully')
    return redirect(userlogin)

def addtocart(request):
        if(request.method == "POST"):

            if(request.user.is_authenticated):

                pid = int(request.POST.get('pid'))
                pqty =  int(request.POST.get('pqty'))
                uid = request.user.id
                user = User.objects.get(id=uid)
                product = Product.objects.get(id=pid)
                try:
                    cart = Cart.objects.get(product=product,user=user)
                    messages.warning(request, 'Product already in cart')
                    return JsonResponse({'status':'Product already in cart'},safe=False)
                except:
                    if(product.quantity >= pqty):
                        cart = Cart()
                        cart.user = user
                        cart.product = product
                        cart.quantity = pqty
                        cart.price = product.selling_price
                        cart.save()
                        messages.success(request, 'Product added to cart')
                        return JsonResponse({'status':'Product added to cart'},safe=False)
                    else:
                        messages.warning(request, 'Only '+ str(product.quantity) + ' available')
                        return JsonResponse({'status': 'Only '+ str(product.quantity) + ' available'},safe=False)
                else:
                    pass
            else:
                messages.error(request, 'Please login to continue')
                return JsonResponse({'status':'Please login to continue'},safe=False)

        return redirect('/')  
 
@login_required(login_url='userlogin')       
def viewcart(request):
    cartitems = Cart.objects.filter(user=request.user.id)
    totalamount = 0
    total = 0
    for item in cartitems:
        totalamount = totalamount + (item.product.selling_price * item.quantity)
        total = totalamount + 40
    return render(request, 'store/viewcart.html',{'cartitems':cartitems,'totalamount': totalamount,'total':total})

def updatecartitem(request):
    if(request.method == "POST"):
        pid = int(request.POST.get('pid'))
        pqty =  int(request.POST.get('pqty'))
        user = User.objects.get(id=request.user.id)
        product = Product.objects.get(id=pid)
        cart = Cart.objects.get(product=product,user=user)
        cart.quantity = pqty
        cart.save()
        return redirect(viewcart)
        messages.success(request, 'Cart updated')
        return JsonResponse({'status':'Cart updated'},safe=False)
        
    return redirect(homepage)

def removecartitem(request):
    if(request.method == "POST"):
        pid = int(request.POST.get('pid'))
        user = User.objects.get(id=request.user.id)
        product = Product.objects.get(id=pid)
        cartitem = Cart.objects.get(product=product,user=user)
        cartitem.delete()
        return redirect(viewcart)
        messages.success(request, 'Cart item deleted')
        return JsonResponse({'status':'Cart item deleted'},safe=False)    
    return redirect(homepage)

@login_required(login_url='userlogin')
def wishlist(request):
    user = User.objects.get(id=request.user.id)
    wishlist = Wishlist.objects.filter(user=user)
    return render(request, 'store/wishlist.html',{'wishlist':wishlist})

def addtowishlist(request):
    if(request.method == "POST"):

            if(request.user.is_authenticated):

                pid = int(request.POST.get('pid'))
                user = User.objects.get(id=request.user.id)
                product = Product.objects.get(id=pid)
                try:
                    wishlist = Wishlist.objects.get(product=product,user=user)
                    messages.success(request, 'Product already in wishlist')
                    return JsonResponse({'status':'Product already in wishlist'},safe=False)
                except:
                        Wishlist.objects.create(user=user,product=product)
                        messages.success(request, 'Product added to wishlist')
                        return JsonResponse({'status':'Product added to wishlist'},safe=False)
                else:
                    pass
            else:
                messages.error(request, 'Please login to continue')
                return JsonResponse({'status':'Please login to continue'},safe=False)

    return redirect(homepage) 


def removewishlistitem(request):
    if(request.method == "POST"):
        pid = int(request.POST.get('pid'))
        user = User.objects.get(id=request.user.id)
        product = Product.objects.get(id=pid)
        wishlistitem = Wishlist.objects.get(product=product,user=user)
        wishlistitem.delete()
        return redirect(wishlist)    
    return redirect(homepage)

@login_required(login_url='userlogin')
def checkout(request):
    cart = Cart.objects.filter(user=request.user.id)  
    for item in cart:
        if(item.quantity > item.product.quantity):
            cartitem = Cart.objects.get(id=item.id) 
            cartitem.delete()
    cartitems = Cart.objects.filter(user=request.user.id)
    totalamount = 0
    total = 0
    for item in cartitems:
        totalamount = totalamount + (item.product.selling_price * item.quantity)
        total = totalamount + 40

    useraccount = Account.objects.filter(user=request.user.id).first()
    return render(request, 'store/checkout.html',{'cartitems':cartitems,'total':total,'totalamount':totalamount,'useraccount':useraccount})

@login_required(login_url='userlogin')
def placeorder(request):
    if(request.method == "POST"):
        
        currentuser = User.objects.filter(id=request.user.id).first()

        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()

        if not Account.objects.filter(user=request.user.id):
            useraccount = Account()
            useraccount.user = User.objects.get(id=request.user.id)
            useraccount.phone = request.POST.get('phone')
            useraccount.address = request.POST.get('address')
            useraccount.city = request.POST.get('city')
            useraccount.state = request.POST.get('state')
            useraccount.country = request.POST.get('country')
            useraccount.zipcode = request.POST.get('zipcode')
            useraccount.save()
        
        neworder = Order()
        neworder.user = User.objects.get(id=request.user.id)
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.zipcode = request.POST.get('zipcode')
        neworder.paymentmode = request.POST.get('paymentmode')
        neworder.paymentid = request.POST.get('paymentid')

        cart = Cart.objects.filter(user=request.user.id)

        carttotal = 0
        for item in cart:
            carttotal = carttotal + (item.product.selling_price * item.quantity)

        neworder.total = carttotal

        trackingid = random.randint(111111111111111,999999999999999)

        while Order.objects.filter(trackingid=trackingid) is None:
            trackingid = random.randint(111111111111111,999999999999999)

        neworder.trackingid = trackingid
        neworder.save()

        for item in cart:
            OrderItems.objects.create(
                order = neworder,
                product = item.product,
                quantity = item.quantity,
                price = item.product.selling_price,
                subtotal = item.product.selling_price * item.quantity
            )

            orderproduct = Product.objects.filter(id=item.product.id).first()
            orderproduct.quantity = orderproduct.quantity - item.quantity
            orderproduct.save()
        
        cart.delete()

        messages.success(request, 'Order has been placed successfully')

        paymode = request.POST.get('paymentmode')
        if(paymode == 'Pay with Paypal'):
            messages.success(request, 'Order has been placed successfully')
            return JsonResponse({'status':'Order has been  placed successfully'},safe=False)

    return redirect(homepage)

@login_required(login_url='userlogin')
def makepayment(request):
    cart = Cart.objects.filter(user=request.user.id)
    total = 0
    for item in cart:
        total = total + (item.product.selling_price * item.quantity)

    return JsonResponse({'total':total})

@login_required(login_url='userlogin')
def myorders(request):
    orders = Order.objects.filter(user=request.user.id)
    
    return render(request, 'store/myorders.html',{'orders':orders})

def vieworder(request,trackingid):
    order = Order.objects.filter(trackingid=trackingid).filter(user=request.user.id).first()
    orderitems = OrderItems.objects.filter(order=order)
    ordertotal = 0
    total = 0
    for item in orderitems:
        ordertotal = ordertotal + (item.price * item.quantity)
        total = ordertotal + 40
    return render(request, 'store/vieworder.html',{'order':order,'orderitems':orderitems,'ordertotal':ordertotal,'total':total})

def productlist(request):
    products = Product.objects.filter(status=0).values_list('name',flat=True)
    productlist = list(products)
    return JsonResponse(productlist,safe=False)

def searchproduct(request):
    if (request.method == 'POST'):
        searcheditem = request.POST.get('searchproduct')
        if(searcheditem == ""):
            return redirect(request.META.get('HTTP_REFERER'))
            
        else: 
            product = Product.objects.filter(name = searcheditem).first() 

            if(product):
                return redirect('viewproduct'+ '/' + str(product.id))
            else:
                messages.info(request, 'Product Not Found')
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


def about(request):
    return render(request, 'store/about.html',{})

def contact(request):
    return render(request, 'store/contact.html',{})