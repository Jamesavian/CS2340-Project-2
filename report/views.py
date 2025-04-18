from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
import calendar
from django.contrib.auth.decorators import login_required
from .models import Transaction, Income, Expense, Budget
from .forms import ReportForm, IncomeForm, ExpenseForm, BudgetForm

@login_required
def transaction_list(request):
    income_form = IncomeForm()
    expense_form = ExpenseForm()
    budget_form = BudgetForm()

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
        elif 'budget_submit' in request.POST:
            budget_form = BudgetForm(request.POST)
            if budget_form.is_valid():
                category = budget_form.cleaned_data['category']
                existing = Budget.objects.filter(user=request.user, category=category).first()
                if existing:
                    existing.amount = budget_form.cleaned_data['amount']
                    existing.save()
                else:
                    budget = budget_form.save(commit=False)
                    budget.user = request.user
                    budget.save()
                return redirect('report.transaction_list')

    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    budgets = Budget.objects.filter(user=request.user)

    category_totals = {}
    for transaction in transactions.filter(expense__isnull=False):
        category_totals[transaction.category] = category_totals.get(transaction.category, 0) + transaction.amount

    date_list = []
    if transactions:
        date_list = dateRange(transactions)

    return render(request, 'report/transaction_list.html', {
        'transactions': transactions,
        'income_form': income_form,
        'expense_form': expense_form,
        'budget_form': budget_form,
        'budgets': budgets,
        'category_totals': category_totals,
        'date_list': date_list
    })

def dateRange(transactions):
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
            current_year += 1
        else:
            current_month += 1

    return date_list

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
            transaction.user = request.user
            transaction.save()
            return redirect('report.transaction_list')
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
