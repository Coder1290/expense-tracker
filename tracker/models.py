from django.db import models
from django.contrib.auth.models import User  # 👤 Import Django's built-in User model

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Rent', 'Rent'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 🔐 Link expense to user
    title = models.CharField(max_length=100)
    amount = models.FloatField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.DateField()

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"