from django.urls import path
from . import views

urlpatterns = [
    path('add_expense', views.add_expense, name='add_expense'),
    path('expense_list', views.expense_list, name='expense_list'),
]

#path('signup', views.signup, name='accounts.signup'),