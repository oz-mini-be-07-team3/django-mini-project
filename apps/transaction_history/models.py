import datetime
from django.db import models
from apps.common.models import CommonModel
from apps.accounts.models import Account


class TransactionHistory(CommonModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE) # 계좌 정보
    # max_digits=18, decimal_places=2 : 소수점 둘째 자리까지 포함한 글자 수는 최대 18자리 까지
    post_transaction_amount = models.DecimalField(max_digits=18, decimal_places=2, default=0) # 거래 후 잔액
    transaction_amount = models.DecimalField(max_digits=18, decimal_places=2) # 거래 금액
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
    transaction_timestamp = models.DateTimeField(db_index=True, default=datetime.datetime.now)
    # db_index=True 는 데이터베이스 인덱스를 생성하는데 주 목적은 검색과 정렬 속도를 향상시킵니다.
    # transaction_timestamp 필드에서 거래를 최신 시간 순으로 정렬할 때 더 빠르게 정렬됩니다.

    def save(self, *args, **kwargs):
        # post_transaction_amount를 동적으로 설정
        if not self.post_transaction_amount:
            self.post_transaction_amount = Account.balance
        super().save(*args, **kwargs)