from . import views
from django.urls import path

urlpatterns = [
    path('income_expense', views.add_income, name='add_income'),
    path('income_list', views.income_list, name='income_list'),
]


'''
urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
]
'''