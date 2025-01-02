from rest_framework import serializers
from .models import Account

class AccountSeriailzer(serializers.ModelSerializer):
    class Meta:
        model = Account # Account 모델을 직렬화
        fields = [ 'user','bank_code','account_number', 'account_type','balance'] # API로 노출할 필드를 정의


