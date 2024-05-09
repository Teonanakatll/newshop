from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import UserLoginForm, UserRegistrationForm, ProfileForm


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, вы успешно вошли в аккаунт!")
                return HttpResponseRedirect(reverse('main:home'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Home - Авторизация',
        'form': form,
    }
    return render(request, 'users/login.html', context)

def registration(request):

    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            # instance получаем все поля формы
            user = form.instance
            auth.login(request, user)
            messages.success(request, f"{user.username}, вы успешно зарегестрировались и вошли в аккаунт!")
            return redirect('main:home')
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Home - Регистрация',
        'form': form,
    }
    return render(request, 'users/registration.html', context)

@login_required
def profile(request):

    if request.method == "POST":
        # Инстанцированием (instantiation) называют процесс (акт) создания на основе класса экземпляра (instance) —
        # такого объекта, который получает доступ ко всему содержимому класса, но при этом обладает и способностью
        # хранить собственные данные.

        # чтобы добавить изображение присваиваем переменной files файл из request

        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        print(request.user)
        if form.is_valid():
            print('yes')
            form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        # заполняем данными текущего пользователя
        form = ProfileForm(instance=request.user)

    context = {
        'title': 'Home - Кабинет',
        'form': form,
    }
    return render(request, 'users/profile.html', context)

@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, вы вышли из аккаунта! ")
    auth.logout(request)

    return redirect('main:home')
