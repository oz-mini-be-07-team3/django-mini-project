from rest_framework import serializers
from apps.transaction_history.models import TransactionHistory


class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = ["account", "transaction_type", "transaction_amount", "transaction_timestamp", "post_transaction_amount"]
        # fields = "__all__"