from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm
from django.db.models import Count
from django.db import transaction
from django.contrib.auth.decorators import login_required

from .models import Civilian, City, Estate
from .forms import CivilianForm


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
                return redirect('/auth/')
    else:
        form = LoginForm()

    return render(request,
                  template_name='auth.html',
                  context={'form': form}
                  )


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
    return render(request,
                  template_name='register.html',
                  context={'user_form': user_form}
                  )


def index(request):
    return render(
        request,
        template_name="index.html",
    )


@login_required(login_url='/auth/')
def show_city(request):
    if not request.user.is_authenticated:
        return redirect('/auth/')

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
    by_estes = request.GET.get('by_estes')
    current_city_name = ""
    current_city_population = ""
    cities = City.objects.all()

    civilians = (Civilian.objects
                 .prefetch_related('vassals')
                 .select_related('estate')
                 .select_related('senior')
                 .order_by('estate')
                 )
    estates = Estate.objects.prefetch_related('civilians')

    if name:
        civilians = civilians.filter(name=name)
    if city:
        city = (City.objects
                .annotate(population=Count('civilians'))
                .prefetch_civilians().get(name=city))
        current_city_name = city.name
        current_city_population = city.population
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
    if by_estes:
        civilians = civilians.order_by('estate')
    if senior:
        civilians = civilians.filter(senior=senior)
    if without_vassals:
        civilians = civilians.filter(vassal=None)

    return render(
        request,
        template_name='city.html',
        context={
            'current_city_population': current_city_population,
            'current_city_name': current_city_name,
            'civilians': civilians,
            'cities': cities,
            'estates': estates,
        })


@transaction.atomic
@login_required(login_url='/auth/')
def view_civilian(request, civilian_id):
    if not request.user.is_authenticated:
        return redirect('/auth/')

    # TODO need to use DRF

    civilian = get_object_or_404((Civilian.objects
                                  .prefetch_related('vassals')
                                  .select_related('estate')
                                  .select_related('senior')
                                  ), id=civilian_id)

    if request.method == 'POST':
        form = CivilianForm(request.POST, instance=civilian)
        if form.is_valid():
            form.save()

        return render(
            request,
            template_name='civilian.html',
            context={
                'form': form,
                'civilian': civilian,
            })

    form = CivilianForm(instance=civilian)

    return render(
        request,
        template_name='civilian.html',
        context={
            'form': form,
            'civilian': civilian,
        })
