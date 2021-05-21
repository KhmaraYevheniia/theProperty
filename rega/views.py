from django.shortcuts import render, redirect
from .models import User
from .forms import UserForm

def index(request):
    users = User.objects.all()
    return render(request, 'rega/index.html')

def registration(request):
    error = ''
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save
            return redirect('login')
        else:
            error = 'Форма заполнена неверно'

    form = UserForm()
    user = {
        'form': form,
        'error': error
    }
    return render(request, 'rega/registration.html', user)


