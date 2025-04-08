from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from .models import Transaction, Income, Expense
from .forms import ReportForm, IncomeForm, ExpenseForm

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'report/transaction_list.html', {'transactions': transactions})

@login_required
def add_transaction(request, formType, templateName):
    if request.method == 'POST':
        form = formType(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user  # link to current user
            transaction.save()
            return redirect('transaction_list')  # or whatever page you want to go to
    elif request.method == 'GET':
        form = formType()
    return render(request, templateName, {'form': form})

@login_required
def add_income(request):
    return add_transaction(request, IncomeForm, 'report/add_income.html')

@login_required
def add_expense(request):
    return add_transaction(request, ExpenseForm, 'report/add_expense.html')