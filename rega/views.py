from django.shortcuts import render, redirect
from .models import User
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    users = User.objects.all()
    if request.user.is_authenticated:
        return render(request, 'rega/index.html', {'users': users})

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
            return redirect('users')
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
                return redirect('users')
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
    return redirect('sign_in')
