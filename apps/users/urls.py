from django.urls import path

from . import views

urlpatterns = [
    path('clients/', views.ClientsView.as_view()),
    path('clients/<int:pk>/', views.ClientsView.as_view()),
]
