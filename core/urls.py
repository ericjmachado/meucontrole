from django.conf.urls import url
from django.urls import include

from . import views

urlpatterns = [
    url('login/', views.LoginView.as_view(), name='login'),
    url('register/', views.RegisterView.as_view(), name='register'),
    url('plan/', views.PlanView.as_view(), name='plan'),
    url('expense/', views.ExpenseView.as_view(), name='expense'),
    url('logout/', views.LogoutView.as_view(), name='logout'),
    url('', include('pwa.urls')),
    url('', views.HomeView.as_view(), name='home'),
]
