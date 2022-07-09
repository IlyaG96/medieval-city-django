from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm

from .models import Civilian, City, Estate


def auth(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/city/')
                else:
                    return redirect('/auth/')
            else:
                return redirect('/city/')
    else:
        form = LoginForm()

    return render(request,
                  template_name='auth.html',
                  context={'form': form})


def user_logout(request):
    logout(request)

    return render(request,
                  template_name='index.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('/auth/')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


def index(request):
    return render(
        request,
        template_name="index.html",
    )


def show_city(request):
    if not request.user.is_authenticated:
        return redirect('/auth/')

    # TODO use select/prefetch related etc.
    name = request.GET.get('name')
    surname = request.GET.get('surname')
    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')
    min_income = request.GET.get('min_income')
    max_income = request.GET.get('max_income')
    estate = request.GET.get('estate')
    senior = request.GET.get('senior')
    without_vassals = request.GET.get('without_vassals')
    city = request.GET.get('city')
    current_city = ""
    cities = City.objects.all()
    civilians = Civilian.objects.all()
    estates = Estate.objects.all()
    names = [civilian.name for civilian in civilians]
    surnames = [civilian.surname for civilian in civilians]

    if name:
        civilians = civilians.filter(name=name)
    if city:
        city = City.objects.get(name=city)
        current_city = city.name
        civilians = civilians.filter(city=city)
    if surname:
        civilians = civilians.filter(surname=surname)
    if min_age:
        civilians = civilians.filter(age__gt=min_age)
    if max_age:
        civilians = civilians.filter(age__lt=max_age)
    if min_income:
        civilians = civilians.filter(income__gt=min_income)
    if max_income:
        civilians = civilians.filter(income__lt=max_income)
    if estate:
        estate = Estate.objects.get(class_name=estate)
        civilians = civilians.filter(estate=estate)
    if senior:
        civilians = civilians.filter(senior=senior)
    if without_vassals:
        civilians = civilians.filter(vassal=None)

    return render(
        request,
        template_name='city.html',
        context={
            'title': current_city,
            'civilians': civilians,
            'cities': cities,
            'names': names,
            'surnames': surnames,
            'estates': estates,
        })


def view_civilian(request, civilian_id):
    current_civilian = Civilian.objects.get(id=civilian_id)

    return render(
        request,
        template_name='civilian.html',
        context={
            'civilian': current_civilian,
        })