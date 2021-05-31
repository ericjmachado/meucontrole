from django.conf.urls import url

from . import views

urlpatterns = [
    url('login/', views.LoginView.as_view(), name='login'),
    url('register/', views.RegisterView.as_view(), name='register'),
    url('home/', views.HomeView.as_view(), name='home'),
]
