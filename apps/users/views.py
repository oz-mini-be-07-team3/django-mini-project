from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


from .models import User
from .serializers import UserSerializer




class UserView(APIView):
	# 모든 유저 조회
	def get(self, request):
		try:
			user = User.objects.all()
			serializer = UserSerializer(user, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		except Exception as e:
			return Response(status=status.HTTP_400_BAD_REQUEST)

	# 회원가입
	def post(self, request):
		# password => 검증 필수, hash화해서 저장 필요
		password = request.data.get('password')
		serializer = UserSerializer(data=request.data) # 역직렬화

		try:
			# 비밀번호 유효성 검사(특수문자 등)
			validate_password(password)
		except:
			raise ParseError("Invalid password")

		if serializer.is_valid(): # 데이터가 유효한지 확인
			user = serializer.save() # 새로운 유저를 생성
			user.set_password(password) # 비밀번호 해쉬화
			user.save()

			serializer = UserSerializer(user) # 직렬화
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 본인 정보 조회/수정/삭제
class UserDetailView(APIView):
	# 튜플은 데이터가 불변이므로 안전하게 튜플로 전달
	authentication_classes = (JWTAuthentication,) # jwt token이 있는지 검증
	permission_classes = (IsAuthenticated,) # 어떤 인증 방식이든 인증된 유저인지 검증

	# 본인의 정보만 조회/수정/삭제가 가능하게 체크
	def check_permission(self, request, pk):
		if request.user.id != pk:
			raise PermissionDenied("권한이 없습니다.")

	# 조회
	def get(self, request, pk):
		self.check_permission(request, pk)  # 예외가 발생하지 않으면 다음으로 진행
		user = get_object_or_404(User, pk=pk) # 값이 없으면 404
		serializer = UserSerializer(user)
		return Response(serializer.data, status=status.HTTP_200_OK)

	# 수정
	def put(self, request, pk):
		self.check_permission(request, pk)
		user = get_object_or_404(User, pk=pk)
		# put은 원래 모든 field를 요청해야하지만 partial로 patch와 같이 일부 필드만 요청해도 수정되도록 만듦
		serializer = UserSerializer(user, data=request.data, partial=True)

		if serializer.is_valid():
			serializer.save()

			return Response(serializer.data)
		else:
			return Response(serializer.errors)

	# 삭제
	def delete(self, request, pk):
		self.check_permission(request, pk)  # 예외가 발생하지 않으면 다음으로 진행
		user = get_object_or_404(User, pk=pk)
		user.delete()
		return Response("delete complete", status=status.HTTP_204_NO_CONTENT)


# 로그인
class JWTLoginView(APIView):
	# 로그인 할 때는 어떠한 인증도 필요없이 post가 가능하게 해줘야함
	permission_classes = (AllowAny,)

	def post(self, request):
		email = request.data.get('email')
		password = request.data.get('password')
		# db에 있는지 사용자 인증
		user = authenticate(request, email=email, password=password)

		# 유저가 있으면 True
		if user is not None:
			refresh = RefreshToken.for_user(user)
			return Response({
				"refresh": str(refresh),
				"access": str(refresh.access_token),
			}, status=status.HTTP_200_OK)
		else:
			return Response({"Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# 로그아웃
class JWTLogoutView(APIView):
# blacklist 기능 - 토큰 유효기간이 지나지 않아도 블랙리스트에 등록(로그아웃)
	authentication_classes = (JWTAuthentication,)  # jwt token이 있는지 검증
	permission_classes = (IsAuthenticated,)  # 어떤 인증 방식이든 인증된 유저인지 검증

	def post(self, request):
		try:
			refresh_token = request.data.get('refresh')
			token = RefreshToken(refresh_token)
			token.blacklist() # refresh token을 blacklist에 추가
			return Response({"Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
		except Exception as e:
			return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)