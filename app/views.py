from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q

class ProductView(View):
    def get(self, request):
        helmet = Product.objects.filter(category = 'Helmet')
        accessories = Product.objects.filter(category = 'Accessories')
        tyres = Product.objects.filter(category = 'Tyres')
        jersey = Product.objects.filter(category = 'Jersey')
        lubricant = Product.objects.filter(category = 'Lubricant')
    
        context = {
            'helmet' : helmet,
            'accessories' : accessories,
            'tyres' : tyres,
            'jersery' : jersey,
            'lubricant' : lubricant,
     }
    
        return render( request, 'app/home.html', context)

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        context = {
            'product' : product
        }
        return render(request, 'app/productdetail.html', context)

def add_to_cart(request):
        user = request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        Cart(user = user, product=product).save()
        if request.user.is_authenticated:
            user =  request.user
            cart = Cart.objects.filter(user=user)
            amount = 0.0
            shipping_amount = 150.0
            total_amount = 0.0
            cart_product = [p for p in Cart.objects.all() if p.user == user]
            print(cart_product)
            if cart_product:
                for p in cart_product:
                    tempamount = (p.quatity * p.product.discounted_price)
                    amount += tempamount
                    totalamount = amount + shipping_amount

            return render(request, 'app/addtocart.html',{
                'cart':cart,
                'shipping_amount' : shipping_amount,
                'totalamount' : totalamount,
                'tempamount' : amount
                })

                
def showCart(request):
    if request.user.is_authenticated:
        user =  request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 150.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quatity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount

            return render(request, 'app/addtocart.html',{
                'cart':cart,
                'shipping_amount' : shipping_amount,
                'totalamount' : totalamount,
                'tempamount' : amount
                })
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quatity+=1
        c.save()
        user =  request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 150.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
    
        for p in cart_product:
            tempamount = (p.quatity * p.product.discounted_price)
            amount += tempamount
        

            data = {
                'quatity' : c.quatity,
                'amount' : amount,
                'totalamount' :  amount + shipping_amount
            }
        return JsonResponse(data)



def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quatity-=1
        c.save()
        user =  request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 150.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
    
        for p in cart_product:
            tempamount = (p.quatity * p.product.discounted_price)
            amount += tempamount
         

            data = {
                'quatity' : c.quatity,
                'amount' : amount,
                'totalamount' : amount + shipping_amount
            }
        return JsonResponse(data)

def removeItem(request):
     if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user =  request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 150.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
    
        for p in cart_product:
            tempamount = (p.quatity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount

            data = {
                'amount' : amount,
                'totalamount' : totalamount
            }
        return JsonResponse(data)













def buy_now(request):
 return render(request, 'app/buynow.html')



def address(request):
    add = Customer.objects.filter(user=request.user)
    context = {
        'add':add,
        'active':'btn-primary',
    }
    return render(request, 'app/address.html',context)

def orders(request):
 return render(request, 'app/orders.html')


def mobile(request, data=None):
    if data == None:
        helmet = Product.objects.filter(category = 'Helmet')    
    elif data == 'LS2' or data == 'Airoh':
        helmet = Product.objects.filter(category = 'Helmet').filter(brand = data)   
    elif data == 'below':
          helmet = Product.objects.filter(category = 'Helmet').filter(discounted_price__lt=10000)   
    elif data == 'above':
        helmet = Product.objects.filter(category = 'Helmet').filter(discounted_price__gt=10000)   
    context = {
        'helmet' : helmet
    }
    return render(request, 'app/mobile.html', context)



class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulation, User Register Successfully')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})

def checkout(request):
 return render(request, 'app/checkout.html')


class ProfileView(View):
     def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',{
            'form':form,
            'active':'btn-primary',
        })
     def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            contactNumber = form.cleaned_data['contactNumber']
            zipcode = form.cleaned_data['zipcode']    
            reg = Customer(
                user=usr,
                name=name,
                locality=locality,
                city=city,
                state=state,
                contactNumber=contactNumber,
                zipcode=zipcode
            )
            reg.save()
            messages.success(request, 'Congratulations! Profile Updated Successfully')
        return render(request, 'app/profile.html', {
            'form':form,
            'active':'btn-primary',
        })