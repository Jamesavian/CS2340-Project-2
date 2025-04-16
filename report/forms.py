from django import forms
from .models import Transaction, Income, Expense, Budget

class ReportForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['source', 'amount', 'date', 'category']

class IncomeForm(ReportForm):
    class Meta:
        model = Income
        fields = ['source', 'amount', 'date', 'category']

class ExpenseForm(ReportForm):
    class Meta:
        model = Expense
        fields = ['source', 'amount', 'date', 'category']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount']
