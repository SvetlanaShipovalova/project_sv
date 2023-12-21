import hashlib
import statistics
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.views import generic
from myProject.models import Order, Customer, Provider, Statistics, Region
from myProject.forms import OrderForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")
def show_info(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name='Заказчики').exists():
            customer = Customer.objects.get(id_user_id=user.id)
            orders = list(Order.objects.filter(customer=customer.id))
            response_data = {
                'customer': customer,
                'orders': orders
            }
            return render(request, 'customerinfo.html', response_data)
        elif user.groups.filter(name='Поставщики').exists():
            provider = Provider.objects.get(id_user_id=user.id)
            statisticss = list(Statistics.objects.filter(provider_id = provider.id))
            orders = Order.objects.filter(provider=provider.id).count()
            response_data = {
                'provider': provider,
                'statisticss': statisticss,
                'orders': orders,
            }
            return render(request, "providerView.html", response_data)
        else:
            return render(request, 'waitAddition.html')
    else:
        return render(request, 'notAccess.html')
def show_customer(request, id_user):
    user = request.user
    if user.is_authenticated:
        customer = Customer.objects.get(id_user_id=request.user.id)
        orders = Order.objects.filter(customer=customer.id)
        orders = list(orders)
        response_data = {
            'customer': customer,
            'orders': orders
        }
        user = request.user
        return render(request, 'customerinfo.html', response_data)

    else:
        return render(request, 'notAccess.html')
def show_index(request):
    if request.method == "GET":
        cur_user = request.user
        if cur_user.is_authenticated:
            return redirect("/info")
        else:
            return render(request, 'mainPage.html')
    else:
        if(request.POST.get("email")!=None):
            email = request.POST.get("email")
            password = request.POST.get("password")
            username = User.objects.get(email=email).username
            user = authenticate(username=username, password=password)
            try:
                login(request, user)
                return redirect("/info")
            except Exception:
                print("Неверно указанный пароль или почта")
                return render(request, 'notAccess.html')
        else:
            email = request.POST.get("create_email")
            username = request.POST.get("create_user_name")
            password = request.POST.get("create_password")
            user = User.objects.create_user(email=email,username=username,password=password)
            login(request,user)
            return redirect("/info")
"""
def create_order(request, id_user):
    if request.method == "GET":
        orderForm = OrderForm()
        return render(request,"formCreateOrder.html",{"form":orderForm})
    else:
        form = OrderForm(request.POST)
        if form.is_valid():
            obj = Order.objects.create(
                customer_id= Customer.objects.get(id_user_id=id_user).id,
                provider_id= Provider.objects.get(id_user_id=request.user),
                number = form.cleaned_data["number"],
                amount = form.cleaned_data["amount"],
                order_date= form.cleaned_data["order_date"]

        else:
            print("ups")
            pass
"""
def create_order(request, id_user):
    orderForm = OrderForm()
    if request.method == "GET":
        return render(request,"formCreateOrder.html",{"form":orderForm})
    else:
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit = False)
            order.customer = Customer.objects.get(id_user_id=request.user.id)
            order.save()
            return redirect(f"/showCustomer/{id_user}")
        else:
            print("ups")
            return redirect("/")
def delete_order(request, id_user, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()
    return redirect(f"/providerView/{id_user}")

def show_CustomerFromProvider(request, id_user):
    user = request.user
    provider = Provider.objects.get(id_user_id=request.user.id)
    orders = Order.objects.filter(provider=provider.id)
    orders = list(orders)
    response_data = {
        'provider': provider,
        'orders': orders
    }
    return render(request, 'providerViewOrder.html', response_data)

def validate_username(request):
    username = request.GET.get('create_user_name', None)
    response = {
        'taken': User.objects.filter(username__exact=username).exists()
    }
    return JsonResponse(response)

def validate_email(request):
    email = request.GET.get('create_email', None)
    response = {
        'taken': User.objects.filter(email__exact=email).exists()
    }
    return JsonResponse(response)

def check_numberOrder(request, id_customer):
    number = int(request.GET.get('number', None))
    customer = Customer.objects.get(id_user_id=request.user.id)
    if (number == ""):
        number = 0
    response = {
        'exist': Order.objects.filter(number=number, customer = customer).exists()
    }
    return JsonResponse(response)

