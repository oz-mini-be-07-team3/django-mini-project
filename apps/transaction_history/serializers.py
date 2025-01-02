from rest_framework import serializers
from apps.transaction_history.models import TransactionHistory


class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = ["id", "account", "transaction_type", "transaction_method", "transaction_amount", "post_transaction_amount", "transaction_timestamp"]
        # fields = "__all__"