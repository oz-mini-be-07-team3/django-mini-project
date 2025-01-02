from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Account
from .serializers import AccountSeriailzer


class AccountListApiView(APIView):    # 계좌 목록 조회 , 생성을 처리함
    authentication_classes = [JWTAuthentication] # 사용자가 로그인해서 받은 JWT 토큰을 확인하여 인증 처리함
    permission_classes = [IsAuthenticated] # 로그인한 사용자만 이 API 사용 가능함
   
   
    def get(self, request): # 계좌 목록 조회
        accounts = Account.objects.filter(user=request.user) # 로그인한 사용자와 관련된 계좌만 필터링
        serializer = AccountSeriailzer(accounts, many=True) #accounts 데이터를 AccountSeriailzer를 사용하여 변환(JSON형식)
        return Response(serializer.data, status=status.HTTP_200_OK) # 요청이 성공적으로 처리, 상태코드 200
    
    def post(self, request): # 새 계좌 생성
        serializer = AccountSeriailzer(data=request.data)
        if serializer.is_valid(): # 데이터가 유효한지 확인
            serializer.save(user=request.user) # 새 계좌가 현재 로그인한 사용자의 계좌로 생성
            return Response(serializer.data, status=status.HTTP_201_CREATED) # 새 계좌 성공적으로 생성, 상태코드 201
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) # 유효하지 않은 데이터가 있을 시 오류 메시지와 상태코드 400
    

class AccountDeleteAPIView(APIView): # 계좌 삭제 처리
    authentication_classes = [JWTAuthentication] # 사용자가 로그인해서 받은 JWT 토큰을 확인하여 인증 처리함
    permission_classes = [IsAuthenticated] # 로그인한 사용자만 이 API 사용 가능함

    def delete(self, request, pk): # 계좌 삭제
        try:
            account = Account.objects.get(pk=pk,user=request.user) # pk는 계좌의 고유 ID, 로그인한 사용자와 관련된 계좌만 삭제
            account.delete() # 해당 계좌 삭제
            return Response({"detail": "Account deleted successfully."}, status=status.HTTP_200_OK) # 삭제 성공 메시지와 상태코드 200(삭제 성공을 의미)
        except Account.DoesNotExist:
            return Response({"detail": "Account not found."}, status=status.HTTP_404_NOT_FOUND) # 해당 계좌를 찾을 수 없다면 찾을 수 없다는 메시지와 상태코드 404


    

    
