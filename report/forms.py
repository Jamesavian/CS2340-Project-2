from django import forms
from .models import Transaction, Income, Expense

class ReportForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['source', 'amount', 'date']

class IncomeForm(ReportForm):
    class Meta:
        model = Income
        fields = ['source', 'amount', 'date']

class ExpenseForm(ReportForm):
    class Meta:
        model = Expense
        fields = ['source', 'amount', 'date', 'category']
