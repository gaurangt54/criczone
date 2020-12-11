from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from .filters import OrderFilter, ProductFilter
from .decorators import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import send_mail
import pywhatkit as kit
from datetime import datetime

now = datetime.now()

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username / Password is incorrect')
            return render(request, "accounts/login.html")

    context = {}
    return render(request, "accounts/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account was created for '+user.username)
            return redirect('login')

    context = {'form':form}
    return render(request, "accounts/register.html", context)

@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def userPage(request):
    cust = Customer.objects.get(name=request.user)
    cart = cust.cart_set.all()
    quantity = 0
    for i in cart:
        quantity += i.quantity
    orders = request.user.customer.order_set.all()
    total = Order.total
    print(total)
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders, 'total_orders':orders.count(), 'delivered':delivered, 'pending':pending,
               'total': total, 'quantity': quantity}
    return render(request, "accounts/user.html", context)


@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def accountSettings(request):
    cust = Customer.objects.get(name=request.user)
    cart = cust.cart_set.all()
    quantity = 0
    for i in cart:
        quantity += i.quantity
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form, 'quantity':quantity}
    return render(request, "accounts/account_settings.html", context)


@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def shop(request):
    cust = Customer.objects.get(name=request.user)
    cart = cust.cart_set.all()
    quantity = 0
    for i in cart:
        quantity += i.quantity
    products = Product.objects.all()
    context = {'products': products, 'quantity': quantity}
    return render(request, "accounts/home.html", context)

@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def category(request,pk):
    cust = Customer.objects.get(name=request.user)
    cart = cust.cart_set.all()
    quantity = 0
    for i in cart:
        quantity += i.quantity
    products = Product.objects.filter(category=pk)
    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs
    context = {'products': products, 'quantity': quantity,
               'category': pk, 'myFilter': myFilter}
    return render(request, "accounts/shop.html", context)

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders, 'customers':customers, 'total_customers':customers.count(), 'total_orders':orders.count(),
                'delivered':delivered, 'pending':pending
    }
    return render(request, "accounts/dashboard.html", context)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, "accounts/products.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'total_orders':orders.count(), 'myFilter':myFilter}
    return render(request, "accounts/customer.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES,)
        if form.is_valid:
            form.save()
            return redirect('products')
    
    context = {'form': form}
    return render(request, 'accounts/create_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateProduct(request,pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST ,request.FILES, instance=product)
        if form.is_valid:
            form.save()
            return redirect('products')
    
    context = {'form': form}
    return render(request, 'accounts/create_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteProduct(request,pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    
    context = {'form': product}
    return render(request, 'accounts/create_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none() ,instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid:
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)  
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, 'accounts/order_form.html', context)

# Create your views here.
@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def addCart(request,pk):
    print(pk)
    customer = Customer.objects.get(name=request.user)
    product = Product.objects.get(id=pk)
    try:
        cart = Cart.objects.get(
            customer=customer, product=product)
        cart.quantity +=1
        cart.save()
        return redirect('view_cart')
    except:
        cart = Cart.objects.create(customer=customer, product=product, quantity=1)
        cart.save()
        cat = product.category
        return redirect('category',cat )

@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def viewCart(request):
    cust = Customer.objects.get(name=request.user)
    cart = cust.cart_set.all()
    quantity = 0
    amount = 0 
    for i in cart:
        quantity += i.quantity
        amount += (i.quantity*i.product.price)
    context = {'cart':cart, 'total_products':cart.count(), 'quantity':quantity, 'amount':amount}
    return render(request, 'accounts/cart.html', context)

@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def deleteCart(request, pk):
    print(pk)
    customer = Customer.objects.get(name=request.user)
    product = Product.objects.get(id=pk)
    try:
        cart = Cart.objects.get(
            customer=customer, product=product)
        if cart.quantity > 1:
            cart.quantity -=1
            cart.save()
        else:
            cart.delete()
        return redirect('view_cart')
    except:
        pass
        return redirect('shop')

@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def checkout(request):
    cust = request.user.customer
    form = CustomerForm(instance=cust)
    cart = cust.cart_set.all()
    quantity = 0
    amount = 0 
    for i in cart:
        quantity += i.quantity
        amount += (i.quantity*i.product.price)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=cust)
        address = request.POST.get('address')
        for i in cart:
            order = Order.objects.create(customer=cust, product=i.product, quantity=i.quantity, address=address, status='Pending')
            order.save()
            cart = Cart.objects.get(customer=cust, product=i.product)
            cart.delete()
            send_mail(
                "Order Confirmation",
                str(f"Thank you {request.user.customer.name} for shopping \n Your order is placed successfully \n Total Bill is {amount}"),
                'mrrobotthebest@gmail.com',
                [request.user.customer.email],
            )
            #kit.sendwhatmsg(str("+91"+str(cust.phone)),
             #               str(f"Thank you {request.user.customer.name} for shopping \n Your order is placed successfully \n Total Bill is {amount}"),
              #              now.hour,(now.minute+2)
#)


        return redirect('user-page')

    context = {'cart': cart, 'customer': cust, 'form': form,
               'total_products': cart.count(), 'quantity': quantity, 'amount': amount}
    return render(request, 'accounts/checkout.html', context)
