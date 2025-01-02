from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.permissions import AllowAny

from apps.transaction_history.models import TransactionHistory
from apps.transaction_history.serializers import TransactionHistorySerializer
from apps.accounts.models import Account
from apps.users.models import User


class TransactionHistoryView(APIView):

    authentication_classes = (JWTAuthentication,)  # jwt token이 있는지 검증
    permission_classes = (IsAuthenticated,)  # 어떤 인증 방식이든 인증된 유저인지 검증

    # 현재 로그인 된 사용자 거래 내역 조회
    def get(self, request):
        # 현재 로그인 된 사용자 정보 가져오기
        user = request.user

        # 사용자와 연결된 계좌 가져오기
        accounts = Account.objects.filter(user=user)
        if not accounts.exists():
            return Response({"error": "사용자 계좌를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 해당 계좌의 모든 거래 내역 조회 - 최근 거래 시간 순으로 정렬
        transactions = TransactionHistory.objects.filter(account__in=accounts).order_by("-transaction_timestamp") # 내림차순
        # account__in 은 account 필드 값이 특정 집합에 포함되는지 확인
        serializer = TransactionHistorySerializer(transactions, many=True) # 거래 내역 직렬화
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 인증되지 않은 사용자를 기본 사용자로 설정 (테스트 환경용)
    # def initial(self, request, *args, **kwargs):
    #     super().initial(request, *args, **kwargs)
    #     if request.user.is_anonymous:
    #         request.user = User.objects.first()  # 첫 번째 사용자 가져오기


class TransactionHistoryAccountView(APIView):

    authentication_classes = (JWTAuthentication,)  # jwt token이 있는지 검증
    permission_classes = (IsAuthenticated,)  # 어떤 인증 방식이든 인증된 유저인지 검증

    # 특정 계좌 거래 내역 조회
    def get(self, request, account_id):
        # 현재 로그인 된 사용자 정보 가져오기
        user = request.user

        # 사용자와 연결된 계좌 가져오기
        accounts = Account.objects.filter(user=user, id=account_id)
        if not accounts.exists():
            return Response({"error": "사용자 계좌를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 해당 계좌의 모든 거래 내역 조회 - 최근 거래 시간 순으로 정렬
        transactions = TransactionHistory.objects.filter(account__in=accounts).order_by("-transaction_timestamp")
        serializer = TransactionHistorySerializer(transactions, many=True) # 거래 내역 직렬화
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 인증되지 않은 사용자를 기본 사용자로 설정 (테스트 환경용)
    # def initial(self, request, *args, **kwargs):
    #     super().initial(request, *args, **kwargs)
    #     if request.user.is_anonymous:
    #         request.user = User.objects.first()  # 첫 번째 사용자 가져오기


class TransactionHistoryCreateView(APIView):

    authentication_classes = (JWTAuthentication,)  # jwt token이 있는지 검증
    permission_classes = (IsAuthenticated,)  # 어떤 인증 방식이든 인증된 유저인지 검증

    # 거래 내역 생성
    def post(self, request):
        # 인증 확인
        if request.user.is_anonymous:
            request.user = User.objects.first()
        #     return Response({"error": "인증이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        # 요청 데이터에서 계좌 ID 확인
        account_id = request.data.get("account")
        if not account_id:
            # 계좌 ID가 요청 데이터에 없으면 400 응답 반환
            return Response({"error": "계좌 ID가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 계좌가 사용자 소유인지 확인
        account = Account.objects.get(id=account_id, user=request.user)
        if not account:
            # 계좌가 사용자 소유가 아닐 경우 403 응답 반환
            return Response({"error": "유효하지 않은 계좌입니다."}, status=status.HTTP_403_FORBIDDEN)

        # 기존 계좌 잔액 가져오기
        current_balance = account.balance

        # 요청 데이터에서 거래 금액 확인
        transaction_amount = request.data.get("transaction_amount")
        if transaction_amount is None:
            return Response({"error": "거래 금액이 필요합니다."},status=status.HTTP_400_BAD_REQUEST)

        # post_transaction_amount 계산
        if request.data.get("transaction_type") == "DEPOSIT":
            # 입금인 경우
            post_transaction_amount = current_balance + transaction_amount
        elif request.data.get("transaction_type") == "WITHDRAW":
            if transaction_amount > current_balance:
                return Response({"error": "잔액이 부족합니다."}, status=status.HTTP_400_BAD_REQUEST)
            post_transaction_amount = current_balance - transaction_amount
        else:
            return Response({"error": "올바른 거래 유형을 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 거래 내역 생성
        serializer = TransactionHistorySerializer(data=request.data)
        if serializer.is_valid():
            # 유효한 데이터이면 저장 / 추가로 계산된 post_transaction_amount 를 저장
            serializer.save(account=account, post_transaction_amount=post_transaction_amount)

            # 계좌 잔액 업데이트
            account.balance = post_transaction_amount
            account.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 인증되지 않은 사용자를 기본 사용자로 설정 (테스트 환경용)
    # def initial(self, request, *args, **kwargs):
    #     super().initial(request, *args, **kwargs)
    #     if request.user.is_anonymous:
    #         request.user = User.objects.first()  # 첫 번째 사용자 가져오기


class TransactionHistoryDetailView(APIView):
    # 인증되지 않은 사용자를 기본 사용자로 설정 (테스트 환경용)
    # def initial(self, request, *args, **kwargs):
    #
    #     super().initial(request, *args, **kwargs)
    #     if request.user.is_anonymous:
    #         request.user = User.objects.first()  # 첫 번째 사용자 가져오기

    authentication_classes = (JWTAuthentication,)  # jwt token이 있는지 검증
    permission_classes = (IsAuthenticated,)  # 어떤 인증 방식이든 인증된 유저인지 검증

    # 특정 거래 내역 수정
    def put(self, request, transaction_id):
        try:
            # 거래 내역 ID로 특정 거래 내역 조회 (로그인된 사용자의 계좌와 연결된 거래만 허용)
            transaction = TransactionHistory.objects.get(id=transaction_id, account__user=request.user)
            # account__user 는 관계 모델의 특정 필드를 지정해서 필터링하거나 값을 가져올 때 사용
            # TransactionHistory 모델의 account 필드는 Account 모델을 참조하는 ForeignKey
            # Account 모델의 user 필드는 User 모델을 참조하는 ForeignKey
            # account__user 는 TransactionHistory 에서 account 를 따라가고, 그 계좌의 user 를 필터링 하는 조건
        except TransactionHistory.DoesNotExist:
            # 거래 내역이 없으면 404 응답 반환
            return Response({"error": "거래 내역을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 데이터 업데이트
        serializer = TransactionHistorySerializer(transaction, data=request.data, partial=True)
        # partial=True 는 부분 업데이트를 허용하여 요청 데이터에 포함된 필드만 업데이트 하고, 나머지는 기존값을 유지
        # partial 옵션을 설정하지 않으면 기본값이 False 가 되어 모든 필드가 포함 되어야 유효성 검증을 통과

        if serializer.is_valid():
            # 데이터가 유효한 경우 저장
            serializer.save()
            # 성공적으로 업데이트 된 데이터 반환
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 특정 거래 내역 삭제
    def delete(self, request, transaction_id):
        try:
            # 특정 거래 내역 조회
            transaction = TransactionHistory.objects.get(id=transaction_id, account__user=request.user)
        except TransactionHistory.DoesNotExist:
            # 거래 내역이 없는 경우
            return Response({"error": "거래 내역을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 거래 내역 삭제
        transaction.delete()
        # 성공 메세지와 함게 200 반환
        return Response({"message": "거래 내역이 성공적으로 삭제되었습니다."}, status=status.HTTP_200_OK)