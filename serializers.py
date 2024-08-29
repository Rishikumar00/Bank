from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Account, Transaction, LoginLogoutHistory

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'user', 'account_name', 'balance']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'transaction_type', 'amount', 'bank_name', 'timestamp']

class LoginLogoutHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginLogoutHistory
        fields = ['id', 'user', 'action', 'timestamp']
