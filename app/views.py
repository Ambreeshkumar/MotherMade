from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerResistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
# Function base decoratores
from django.contrib.auth.decorators import login_required
# Class based decoratores.
from django.utils.decorators import method_decorator


#def home(request):
# return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(categury = 'TW')
        bottomwears = Product.objects.filter(categury = 'BW')
        mobile = Product.objects.filter(categury = 'M')
        laptop = Product.objects.filter(categury = 'L')
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
        return render(request, 'app/home.html',
            {'topwears':topwears, 'bottomwears':bottomwears, 'mobile':mobile, 'laptop':laptop, 'totalitem':totalitem})
    
    
        



#def product_detail(request):
# return render(request, 'app/productdetail.html')

class ProductDetaileView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user = request.user)).exists()
        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart})

    


#Add to Cart.
@login_required 
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')
    

# Show_Cart.
@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0.0
        shipping_amount = 70.0
        totle_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user] 
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount 
                totleamount = amount + shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart, 'totleamount':totleamount, 
                                'amount':amount, 'totalitem':totalitem})
        else:
            return render(request, 'app/emptycart.html')
 
 
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount 
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totleamount': amount + shipping_amount
            }
    return JsonResponse(data)



 
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount 
            
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totleamount':amount + shipping_amount
            }
    return JsonResponse(data)



 
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount 
           
        data = {
            'amount': amount,
            'totleamount': amount + shipping_amount
            }
    return JsonResponse(data)
            
           


def buy_now(request):
 return render(request, 'app/buynow.html')


#Address.
@login_required
def address(request):
    add = Customer.objects.filter(user = request.user)
    return render(request, 'app/address.html',{'add':add, 'active':'btn-primary'})

#Order.
@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user = request.user)
    return render(request, 'app/orders.html',{'order_placed':op})


# Mobile filter.            
def mobile(request, data = None):
    if data == None:
        mobiles = Product.objects.filter(categury = 'M')
    elif data == 'Redmi' or data == 'samsung':          
        mobiles = Product.objects.filter(categury = 'M').filter(brand = data)
    elif data == 'below':
        mobiles = Product.objects.filter(categury = 'M').filter(discounted_price__lt = 1000)
    elif data == 'above':
        mobiles = Product.objects.filter(categury = 'M').filter(discounted_price__gt = 1000)
    # Cart_count
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    
    return render(request, 'app/mobile.html', {'mobiles':mobiles, 'totalitem':totalitem})

# Laptop
def Laptop(request, data = None):
    if data == None:
        laptop = Product.objects.filter(categury = 'L')
    elif data == 'Apple-MacBook' or data == 'Dell' or data == 'hp':
        laptop = Product.objects.filter(categury = 'L').filter(brand = data)
    elif data == 'below':
        laptop = Product.objects.filter(categury = 'L').filter(discounted_price__lt = 30000)
    elif data == 'above':
        laptop = Product.objects.filter(categury = 'L').filter(discounted_price__gt = 30000)
        
    # Cart_count
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    
    return render(request, 'app/Laptop.html',{'laptop':laptop, 'totalitem':totalitem})


# Top Wear Filter.                              
def Top_Wear(request, data = None):
    if data == None:
        TopWear = Product.objects.filter(categury = 'TW')
    elif data == 'Spker' or data == 'Park' or data == 'polo':
        TopWear = Product.objects.filter(categury = 'TW').filter(brand = data)    
    elif data == 'below': 
        TopWear = Product.objects.filter(categury = 'TW').filter(discounted_price__lt = 500)
    elif data == 'above':
        TopWear = Product.objects.filter(categury = 'TW').filter(discounted_price__gt=500)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    return render(request, 'app/TopWear.html', {'TopWear':TopWear, 'totalitem':totalitem})



# Bottom Wear filter.   
def Bottom_Wear(request, data = None):
    if data == None:
        BottomWear = Product.objects.filter(categury = 'BW')
    elif data == 'Spker' or data == 'Lee':
        BottomWear = Product.objects.filter(categury = 'BW').filter(brand = data)
    elif data == 'below':
        BottomWear = Product.objects.filter(categury = 'BW').filter(discounted_price__lt = 500)
    elif data == 'above':
        BottomWear = Product.objects.filter(categury = 'BW').filter(discounted_price__gt = 500)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    return render(request, 'app/BottomWear.html', {'BottomWear':BottomWear, 'totalitem':totalitem})



# Registration.
class CustomerResistrationView(View):
    def get(self, request):
        form = CustomerResistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    def post(self, request):
        form = CustomerResistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Conratulations!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})


# checkout.
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user = user)
    cart_item = Cart.objects.filter(user = user)
    amount = 0.0
    shipping_amount = 70.0
    totleamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user] 
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount 
            totleamount = amount + shipping_amount
            
    # cart_count 
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    return render(request, 'app/checkout.html', {'add':add, 'totleamount':totleamount, 
                                'cart_item':cart_item, 'totalitem':totalitem})



# payment_done.
@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id = custid)
    cart = Cart.objects.filter(user = user)
    for c in cart:
        OrderPlaced(user = user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")
    



# Profile.
@method_decorator(login_required, name= 'dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']      
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)   
            reg.save()       
            messages.success(request, 'Congratulation!! Profile Updated Successfully')    
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
           
           
           
           
"""           
if request.user.is_authenticated:
            user = request.user
            product_count = Cart.objects.filter(user=user).count()
"""