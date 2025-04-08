from . import views
from django.urls import path

urlpatterns = [
    path('', views.transaction_list, name='report.transaction_list'),
    path('add_income/', views.add_income, name='report.add_income'),
    path('add_expense/', views.add_expense, name='report.add_expense'),
    path('<int:id>/delete_transaction/', views.delete_transaction, name='report.delete_transaction'),
]

#path('signup', views.signup, name='accounts.signup'),