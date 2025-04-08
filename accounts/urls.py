from django.urls import path
from . import views

app_name = 'accounts'

from django.contrib.auth.views import (
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('password-reset/', PasswordResetView.as_view(template_name='accounts/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name='password_reset_complete'),
]
