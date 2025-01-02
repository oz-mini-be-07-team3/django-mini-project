from django.urls import path
from .views import TransactionHistoryView, TransactionHistoryDetailView, TransactionHistoryDetailAccountView, TransactionHistoryCreateView

urlpatterns = [
    path('', TransactionHistoryView.as_view(), name='transaction-list'),
    path('create/', TransactionHistoryCreateView.as_view(), name='transaction-create'),
    path('get/<int:account_id>/', TransactionHistoryDetailAccountView.as_view(), name='transaction-detail-account'),
    path('<int:transaction_id>/', TransactionHistoryDetailView.as_view(), name='transaction-detail')
]