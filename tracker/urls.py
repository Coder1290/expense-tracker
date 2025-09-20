from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Default landing page
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_expense, name='add-expense'),
    path('signup/', views.signup_view, name='signup'),  # 🔓 Signup
    # 🔐 Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]