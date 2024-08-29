# from django.db import models

# # Create your models here.
# from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.utils import timezone

# class User(AbstractUser):
#     pass  # Extending the default User model, you can add custom fields if needed.

# class Account(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
#     account_name = models.CharField(max_length=100)
#     balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     def deposit(self, amount):
#         self.balance += amount
#         self.save()

#     def withdraw(self, amount):
#         if self.balance >= amount:
#             self.balance -= amount
#             self.save()
#         else:
#             raise ValueError("Insufficient funds")

# class Transaction(models.Model):
#     account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
#     transaction_type = models.CharField(max_length=10)  # 'deposit' or 'withdraw'
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     bank_name = models.CharField(max_length=100)
#     timestamp = models.DateTimeField(default=timezone.now)

# class LoginLogoutHistory(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_logout_history')
#     action = models.CharField(max_length=10)  # 'login' or 'logout'
#     timestamp = models.DateTimeField(default=timezone.now)
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    pass  # Extending the default User model, you can add custom fields if needed.

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def deposit(self, amount):
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
        else:
            raise ValueError("Insufficient funds")

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10)  # 'deposit' or 'withdraw'
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bank_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)

class LoginLogoutHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_logout_history')
    action = models.CharField(max_length=10)  # 'login' or 'logout'
    timestamp = models.DateTimeField(default=timezone.now)
