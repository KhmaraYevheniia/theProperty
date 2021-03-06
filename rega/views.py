from typing import Collection
from django.shortcuts import render, redirect
from .models import Contract, User, PropertyObject
from .forms import LoginForm, RegistrationForm, PropertyObjectForm, PropertyContractForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Min, Sum
from django.core.paginator import Paginator
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse

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
          'total_income': round(total_income['price__sum']*0.3)
        }
        return render(request, 'rega/index.html', context)

def contracts(request):
    page_number_contracts = request.GET.get('page') or 1
    property_contracts = Contract.objects.all().order_by('-id')
    current_page_contracts = Paginator(property_contracts, 12)
    page_contracts = current_page_contracts.get_page(page_number_contracts)
    user_contract = User.objects.all()
    property_contracts_count = property_contracts.count()
    context = {
        'property_contracts': page_contracts,
        'user_contract': user_contract,
        'property_contracts_count': property_contracts_count
    }
    return render(request, 'rega/contracts.html', context)

def objects(request):
    page_number = request.GET.get('page') or 1
    search_param = request.GET.get('search') or None
    type_param = request.GET.get('type') or None
    sold_status_param = request.GET.get('sold_status') or None
    price_param = request.GET.get('less_price') or None

    if search_param:
        property_objects = PropertyObject.objects.filter(address__icontains=search_param).order_by('-id')
    elif type_param:
        property_objects = PropertyObject.objects.filter(type__in=type_param.split(',')).order_by('-id')
    elif sold_status_param:
        property_objects = PropertyObject.objects.filter(sold_status__in=sold_status_param.split(',')).order_by('-id')
    elif price_param:
        property_objects = PropertyObject.objects.filter(price__lte=price_param).order_by('-price')
    else:
        property_objects = PropertyObject.objects.all().order_by('-id')

    all_types = PropertyObject.objects.values('type').distinct()
    current_page = Paginator(property_objects, 12)
    page_obj = current_page.get_page(page_number)
    property_objects_count = property_objects.count()

    if request.is_ajax():
        html = render_to_string(
            template_name="rega/objects-results-partial.html",
            context = {
                'property_objects': page_obj,
                'property_objects_count': property_objects_count,
                'search_param': search_param,
                'type_param': type_param
            }
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    context = {
        'property_objects': page_obj,
        'property_objects_count': property_objects_count,
        'all_types': all_types
    }
    return render(request, 'rega/objects.html', context)

def staff(request):
    page_number_staff = request.GET.get('page') or 1
    property_staff = User.objects.all()
    current_page_staff = Paginator(property_staff, 5)
    page_staff = current_page_staff.get_page(page_number_staff)
    property_staff_count = property_staff.count()
    context = {
        'property_staff': page_staff,
        'property_staff_count': property_staff_count
    }
    return render(request, 'rega/staff.html', context)

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
                return redirect('objects')
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
            error = '?????????? ?????????????????? ??????????????. ???????????????????? ?????? ??????'
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
            error = '???????????? ?????? ?????????? ???? ??????????????????!'
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
