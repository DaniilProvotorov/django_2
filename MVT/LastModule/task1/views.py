from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegister
from .models import *


def home(request):
    return render(request, 'homepage.html')


def cats(request):
    games = Game.objects.all()
    context = {
        'games': games
    }
    return render(request, 'cats.html', context)


def func(request):
    list_f = ["Записаться на посещение", "Внести пожертвование", "Приручить питомца"]
    context = {
        "list_f": list_f,
    }
    return render(request, 'func.html', context)


def sign_up_by_html(request):
    users = [user.name for user in Buyer.objects.all()]
    info = {}
    context = {
        "info": info
    }
    if request.method == 'POST':
        username = str(request.POST.get('username'))
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = int(request.POST.get('age'))
        balance = request.POST.get('balance')

        if password == repeat_password and age >= 18 and username not in users:
            Buyer.objects.create(name=username, balance=1000, age=age)#сделал баланс 1000 изначально у всех, не было прописано в задании
            return HttpResponse(f'Приветсвуем, {username}!')
        if password != repeat_password:
            info['error'] = 'Пароли не совпадают'
        if age < 18:
            info['error'] = 'Вы должны быть старше 18'
        if username in users:
            info['error'] = 'Пользователь уже существует'

    return render(request, 'registration_page.html', context)


def sign_up_by_django(request):
    users = [user.name for user in Buyer.objects.all()]
    info = {}
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = int(form.cleaned_data['age'])

            if password == repeat_password and age >= 18 and username not in users:
                Buyer.objects.create(name=username,balance=1000, age=age)
                return HttpResponse(f'Приветсвуем, {username}!')
            if password != repeat_password:
                info['error'] = 'Пароли не совпадают'
            if age < 18:
                info['error'] = 'Вы должны быть старше 18'
            if username in users:
                info['error'] = 'Пользователь уже существует'
    else:
        form = UserRegister()

    return render(request, 'registration_page.html', {'form': form, "info": info})





