from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm
from .models import Expense

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # link to current user
            expense.save()
            return redirect('expense_list')  # or whatever page you want to go to
    elif request.method == 'GET':
        form = ExpenseForm()
    return render(request, 'Expense/add_expense.html', {'form': form})


@login_required
def expense_list(request):

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # link to current user
            expense.save()
            return redirect('expense_list')  # or whatever page you want to go to
    else:
        form = ExpenseForm()
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'Expense/expense_list.html', {'expenses': expenses, 'form': form})