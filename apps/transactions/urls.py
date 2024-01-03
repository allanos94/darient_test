from django.urls import path

from . import views

urlpatterns = [
    path('transactions/', views.TransactionsView.as_view()),
    path('transactions/<int:pk>/', views.TransactionsView.as_view()),
    path('transactions/validate/', views.ValidateView.as_view()),
]
