import calendar

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import *


def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)

            login(request, user)

            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required(login_url='/login')
def home(request):
    return render(request, 'measures/home.html', {})


@login_required(login_url='/login')
def store(request):
    if request.method == 'POST':
        measure_form = MeasureForm(request.POST)

        if measure_form.is_valid():
            measure = measure_form.save(commit=False)
            measure.user = request.user
            measure.save()

            messages.success(request, 'Measurement has been added.')
            return redirect('/')
    else:
        measure_form = MeasureForm()
    return render(request, 'tracker/home.html', {'measure_form': measure_form})


@login_required(login_url='/login')
@api_view(['GET'])
def annual_measures(request):
    measures = []
    for measure in request.user.measure_set.get_annual_averages():
        measures.append({
            'year': measure[0],
            'weight': measure[1]
        })
    data = {
        'measures': measures
    }
    return Response(data)


@login_required(login_url='/login')
@api_view(['GET'])
def monthly_measures(request, year):
    measures = []
    for measure in request.user.measure_set.get_monthly_averages_of_year(year):
        measures.append({
            'month': measure[0],
            'month_name': calendar.month_name[measure[0]],
            'weight': measure[1]
        })
    data = {
        'measures': measures
    }
    return Response(data)


@login_required(login_url='/login')
@api_view(['GET'])
def daily_measures(request, year, month):
    measures = []
    for measure in request.user.measure_set.from_year(year).from_month(month):
        measures.append({
            'date': measure.date,
            'weight': measure.weight
        })
    data = {
        'measures': measures
    }
    return Response(data)
