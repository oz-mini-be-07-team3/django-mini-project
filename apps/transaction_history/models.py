from django.db import models


class TransactionHistory(models.Model):
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE) # 계좌 정보
    post_transaction_amount = models.DecimalField(max_digits=18, decimal_places=2) # 거래 금액
    transaction_amount = models.DecimalField(max_digits=18, decimal_places=2) # 거래 후 잔액
    transaction_method = models.CharField(
        max_length=30,
        choices=[
            ("ATM", "ATM 거래"),
            ("TRANSFER", "계좌이체"),
            ("AUTOMATIC_TRANSFER", "자동이체"),
            ("CARD", "카드결제"),
            ("INTEREST", "이자"),
        ])
    transaction_type = models.CharField(
        max_length=30,
        choices=
        [
            ("DEPOSIT", "입금"),
            ("WITHDRAW", "출금"),
        ]) # 입출금 타입
    transaction_timestamp = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)