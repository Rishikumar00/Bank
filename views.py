from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from .models import Account, Transaction, LoginLogoutHistory
from .serializers import UserSerializer, AccountSerializer, TransactionSerializer, LoginLogoutHistorySerializer

class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        print("*******")
        print(user)
        print("******")
        if user is not None:
            login(request, user)
            LoginLogoutHistory.objects.create(user=user, action='login')
            return Response({"message": "Logged in successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        LoginLogoutHistory.objects.create(user=request.user, action='logout')
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class AccountListView(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.accounts.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionHistoryView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(account__user=self.request.user)

class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        account = Account.objects.get(pk=pk, user=request.user)
        amount = request.data.get('amount')
        bank_name = request.data.get('bank_name')
        account.deposit(float(amount))
        Transaction.objects.create(account=account, transaction_type='deposit', amount=amount, bank_name=bank_name)
        return Response({"message": "Deposit successful", "new_balance": account.balance}, status=status.HTTP_200_OK)

class WithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        account = Account.objects.get(pk=pk, user=request.user)
        amount = request.data.get('amount')
        bank_name = request.data.get('bank_name')
        try:
            account.withdraw(float(amount))
            Transaction.objects.create(account=account, transaction_type='withdraw', amount=amount, bank_name=bank_name)
            return Response({"message": "Withdrawal successful", "new_balance": account.balance}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginLogoutHistoryView(generics.ListAPIView):
    serializer_class = LoginLogoutHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.login_logout_history.all()
