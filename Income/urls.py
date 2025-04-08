from . import views
from django.urls import path

urlpatterns = [
    path('income/add/', views.add_income, name='add_income'),
    path('income/list/', views.income_list, name='income_list'),
]