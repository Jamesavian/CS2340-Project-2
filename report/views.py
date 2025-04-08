from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from .models import Transaction, Income, Expense
from .forms import ReportForm, IncomeForm, ExpenseForm

@login_required
def transaction_list(request):
    income_form = IncomeForm()
    expense_form = ExpenseForm()

    if request.method == 'POST':
        if 'income_submit' in request.POST:
            income_form = IncomeForm(request.POST)
            if income_form.is_valid():
                income = income_form.save(commit=False)
                income.user = request.user
                income.save()
                return redirect('report.transaction_list')
        elif 'expense_submit' in request.POST:
            expense_form = ExpenseForm(request.POST)
            if expense_form.is_valid():
                expense = expense_form.save(commit=False)
                expense.user = request.user
                expense.save()
                return redirect('report.transaction_list')

    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'report/transaction_list.html', {'transactions': transactions,
                                                            'income_form': income_form, 'expense_form': expense_form})

@login_required
def add_transaction(request, formType, templateName):
    if request.method == 'POST':
        form = formType(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            if formType == IncomeForm:
                transaction.type = 'Income'
            else:
                transaction.type = 'Expense'
            transaction.user = request.user  # link to current user
            transaction.save()
            return redirect('report.transaction_list')  # or whatever page you want to go to
    elif request.method == 'GET':
        form = formType()
    return render(request, templateName, {'form': form})

@login_required
def add_income(request):
    return add_transaction(request, IncomeForm, 'report/add_income.html')

@login_required
def add_expense(request):
    return add_transaction(request, ExpenseForm, 'report/add_expense.html')