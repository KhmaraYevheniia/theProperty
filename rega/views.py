from typing import Collection
from django.shortcuts import render, redirect
from .models import Contract, User, PropertyObject
from .forms import LoginForm, RegistrationForm, PropertyObjectForm, PropertyContractForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Min, Sum

@login_required
def index(request):
    property_objects = PropertyObject.objects.all().order_by('-id')
    objects_quantity = property_objects.count()
    unsold_objects_quantity = PropertyObject.objects.filter(sold_status=False).count()
    sold_objects_quantity = objects_quantity - unsold_objects_quantity
    total_income = PropertyObject.objects.aggregate(Sum('price'))

    if request.user.is_authenticated:
        context = {
          'unsold_objects_quantity': unsold_objects_quantity,
          'objects_quantity': objects_quantity,
          'property_objects': property_objects[:14],
          'sold_objects_quantity': sold_objects_quantity,
          'total_income': round(total_income['price__sum'])
        }
        return render(request, 'rega/index.html', context)

def contracts(request):
    property_contracts = Contract.objects.all().order_by('-id')
    user_contract = User.objects.all()
    property_contracts_count = property_contracts.count()
    context = {
        'property_contracts': property_contracts,
        'user_contract': user_contract,
        'property_contracts_count': property_contracts_count
    }
    return render(request, 'rega/contracts.html', context)

def objects(request):
    property_objects = PropertyObject.objects.all().order_by('-id')
    property_objects_count = property_objects.count()
    context = {
        'property_objects': property_objects,
        'property_objects_count': property_objects_count
    }
    return render(request, 'rega/objects.html', context)

@login_required
def create_object(request):
    error = ''
    if request.method == 'POST':
        form = PropertyObjectForm(request.POST)
        longitude = validate_numeric_form(request.POST["longitude"])
        latitude = validate_numeric_form(request.POST["latitude"])
        square = validate_numeric_form(request.POST["square"])
        price = validate_numeric_form(request.POST["price"])
        if longitude and latitude and square and price:
            if form.is_valid():
                new_object = form.save(commit=False)
                new_object.save()
                return redirect('dashboard')
            else:
                error = 'Not all required fields are filled!'
                context = {
                    'form': form,
                    'error': error,
                    'form_name': 'Create new property object'
                    }
                return render(request, 'rega/create_object.html', context)
        else:
            error = 'The data type of the entered fields are not correct!'
            context = {
                'form': form,
                'error': error,
                'form_name': 'Create new property object'
                }
            return render(request, 'rega/create_object.html', context)


    form = PropertyObjectForm()
    context = {
        'form': form,
        'error': error,
        'form_name': 'Create new property object'
    }
    if request.method == 'GET':
        return render(request, 'rega/create_object.html', context)

@login_required
def create_contract(request):
    error = ''
    collection_objects = PropertyObject.objects.all()

    if request.method == 'POST':
        form = PropertyContractForm(request.POST)
        user_creator = User.objects.get(id=request.POST.get('users'))
        property_object = request.POST["property_object"]
        sale_date = request.POST["sale_date"]
        seller_name = request.POST["seller_name"]
        users = request.POST["users"]
        if property_object and sale_date and seller_name and users:
            if form.is_valid():
                new_contract = form.save(commit=False)
                new_contract.save()
                new_contract.users.add(user_creator)
                PropertyObject.objects.filter(id=new_contract.property_object_id).update(sold_status=True)
                return redirect('contracts')
            else:
                error = 'Not all required fields are filled!'
                context = {
                    'form': form,
                    'error': error,
                    'form_name': 'Create new contract'
                    }
                return render(request, 'rega/create_contract.html', context)
        else:
            error = 'The data type of the entered fields are not correct!'
            context = {
                'form': form,
                'error': error,
                'form_name': 'Create new contract'
                }
            return render(request, 'rega/create_contract.html', context)

    form = PropertyContractForm()
    context = {
        'form': form,
        'users': User.objects.all(),
        'form_name': 'Create new contract',
        'collection_objects': collection_objects,
        'error': error
    }
    if request.method == 'GET':
        return render(request, 'rega/create_contract.html', context)

def registration(request):
    error = ''

    if request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            auth_user = authenticate(username=new_user.username, password=form.cleaned_data['password'])
            login(request, auth_user)
            return redirect('dashboard')
        else:
            error = 'Форма заполнена неверно. Попробуйте еще раз'
            context = {
                'form': form,
                'error': error
            }
            return render(request, 'rega/registration.html', context)


    form = RegistrationForm()
    context = {
        'form': form,
        'error': error
    }
    if request.method == 'GET':
        return render(request, 'rega/registration.html', context)


def sign_in(request):
    error = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        context = {
            'form': form,
            'error': error
        }

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.get(email=email)
            auth_user = authenticate(username=user.username, password=password)
            # breakpoint()
            if auth_user:
                login(request, auth_user)
                return redirect('dashboard')
        else:
            error = 'Пароль или емайл не корректны!'
            context = {
                'form': form,
                'error': error
            }
            return render(request, 'rega/sign_in.html', context)


    form = LoginForm()
    context = {
        'form': form,
        'error': error
    }
    if request.method == 'GET':
        return render(request, 'rega/sign_in.html', context)

@login_required
def sign_out(request):
    logout(request)
    return redirect('/sign_in')

def validate_numeric_form(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
