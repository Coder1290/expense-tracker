from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django import forms
from collections import defaultdict
import calendar
import json

from .models import Expense

# -------------------- Views --------------------

# 🔐 Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Already logged in

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        # Optional: Add success message
        # from django.contrib import messages
        # messages.success(request, f"Welcome back, {user.username}!")
        return redirect('dashboard')
    return render(request, 'tracker/login.html', {'form': form})

# 🔓 Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# signup view 
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)  # Auto-login after signup
        return redirect('dashboard')
    return render(request, 'tracker/signup.html', {'form': form})

# 🏠 Home Page
def home(request):
    return render(request, 'tracker/home.html')

# 📝 Expense Form
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

# ➕ Add Expense View (Protected)
@login_required
def add_expense(request):
    form = ExpenseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user  # Link expense to logged-in user
        expense.save()
        return redirect('add-expense')
    return render(request, 'tracker/add_expense.html', {'form': form})

# 📊 Dashboard View with Chart Data (Protected)
@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # -------------------- Pie Chart Data --------------------
    category_totals = defaultdict(float)
    for exp in expenses:
        category_totals[exp.category] += exp.amount

    chart_labels = json.dumps(list(category_totals.keys()))
    chart_data = json.dumps(list(category_totals.values()))

    # -------------------- Bar Chart Data --------------------
    monthly_totals = (
        expenses
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    bar_labels = [calendar.month_abbr[item['month'].month] for item in monthly_totals]
    bar_data = [item['total'] for item in monthly_totals]

    # -------------------- Pass Data to Template --------------------
    context = {
        'expenses': expenses,
        'total': total,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'bar_labels': json.dumps(bar_labels),
        'bar_data': json.dumps(bar_data),
    }

    return render(request, 'tracker/dashboard.html', context)