from django.urls import path
from .views import TransactionHistoryView, TransactionHistoryDetailView, TransactionHistoryAccountView, TransactionHistoryCreateView

urlpatterns = [
    path('', TransactionHistoryView.as_view(), name='transaction-list'),
    path('create/', TransactionHistoryCreateView.as_view(), name='transaction-create'),
    path('account/<int:account_id>/', TransactionHistoryAccountView.as_view(), name='transaction-account'),
    path('<int:transaction_id>/', TransactionHistoryDetailView.as_view(), name='transaction-detail')
]