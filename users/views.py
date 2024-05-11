from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from carts.models import Cart
from .forms import UserLoginForm, UserRegistrationForm, ProfileForm


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            # проводим аутентификацию пользователя
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            # если пользователь существует в бд
            if user:
                # логинимся
                auth.login(request, user)
                messages.success(request, f"{username}, вы успешно вошли в аккаунт!")

                # если пользователь добавлял товары не авторизуясь, во время авторизации добавляем их через session_key
                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                # проверим если пользователь был перенаправлен на этот контроллер (@login_required)
                # отправляем его на страницу указанную в hidden-input
                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))
                # if request.POST.get('next', None):
                #
                #     return HttpResponseRedirect(request.POST.get('next'))

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

            session_key = request.session.session_key

            # instance получаем все поля формы
            user = form.instance
            auth.login(request, user)

            # если пользователь добавлял товары не регистрируясь, во время регистрации добавляем их через session_key
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

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
    messages.success(request, f"{request.user.username}, вы вышли из аккаунта!")
    auth.logout(request)

    return redirect('main:home')

def users_cart(request):
    return render(request, 'users/users_cart.html')
