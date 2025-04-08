from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth.decorators import login_required
from .models import Income
from .forms import IncomeForm


@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  # link to current user
            income.save()
            return redirect('income_list')  # or whatever page you want to go to
    elif request.method == 'GET':
        form = IncomeForm()
    return render(request, 'add_income.html', {'form': form})


@login_required
def income_list(request):
    Income = Income.objects.filter(user=request.user).order_by('-date')
    return render(request, 'Income_list.html', {'income': income})
