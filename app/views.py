from django.shortcuts import render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages

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
 return render(request, 'app/addtocart.html')

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