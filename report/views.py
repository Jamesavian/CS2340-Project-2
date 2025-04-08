from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
import calendar
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

    # Find starting month and year, and ending month and year. Then create a dropdown iterating from every month between them
    date_list = dateRange(transactions)

    return render(request, 'report/transaction_list.html', {'transactions': transactions,
                                        'income_form': income_form, 'expense_form': expense_form, 'date_list': date_list})

def dateRange(transactions):
    # [April 2024, May 2024]
    start_month = transactions[0].date.month
    start_year = transactions[0].date.year
    end_month = transactions.last().date.month
    end_year = transactions.last().date.year

    month_list = list(calendar.month_name)

    date_list = []
    current_month = start_month
    current_year = start_year
    while current_month <= end_month and current_year <= end_year:
        date_list.append(month_list[current_month] + " " + str(current_year))
        if current_month == 12:
            current_month = 1
            current_year = current_year + 1
        else:
            current_month = current_month + 1

    return date_list

@login_required
def add_transaction(request, formType, templateName):
    if request.method == 'POST':
        form = formType(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            if formType == IncomeForm:
                transaction.type = 'Income'
                transaction.save()
            else:
                transaction.type = 'Expense'
                transaction.save()
            transaction.user = request.user  # link to current user
            transaction.save()
            return redirect('report.transaction_list')  # or whatever page you want to go to
    elif request.method == 'GET':
        form = formType()
    return render(request, templateName, {'form': form})

@login_required
def delete_transaction(request, id):
    transaction = get_object_or_404(Transaction, id=id, user=request.user)
    transaction.delete()
    return redirect('report.transaction_list')

@login_required
def add_income(request):
    return add_transaction(request, IncomeForm, 'report/add_income.html')

@login_required
def add_expense(request):
    return add_transaction(request, ExpenseForm, 'report/add_expense.html')