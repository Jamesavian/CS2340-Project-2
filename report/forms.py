from django import forms
from .models import Transaction, Income, Expense

class ReportForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['source', 'amount', 'date']

class IncomeForm(ReportForm):
    model = Income

class ExpenseForm(ReportForm):
    model = Expense