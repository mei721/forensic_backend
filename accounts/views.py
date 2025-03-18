from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializers import *
from forensicapp.pagination import  CustomPaginationWithResult
from .permissions import IsAdmin
import logging


logger = logging.getLogger('accounts')  # logger defined in settings


class RegisterView(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"User registration failed: {serializer.errors}")
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user, tokens = serializer.save()

        logger.info(f"New user registered: {user.email} ({user.username})")

        return Response({
            "data": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "refresh_token": tokens["refresh"],
                "access_token": tokens["access"],
            }
        }, status=status.HTTP_201_CREATED)

    


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            user = self.get_user_from_request(request)  # Custom method to retrieve user
            tokens = response.data  # Contains refresh and access tokens
            print(request.data)
            logger.info(f"User logged in: ({user.username})")

            response.data = {
                "data": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "phone_number": user.phone_number,
                        "refresh_token": tokens.get("refresh"),
                        "access_token": tokens.get("access"),
                }
            }
            return response
        
        except Exception as e:
            logger.error(f"User login failed: {str(e)}")
            return Response({"data": {"error": str(e)}}, status=status.HTTP_400_BAD_REQUEST)
        
    def get_user_from_request(self, request):
        """Retrieve the user from the validated data in the serializer."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.user
    

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"User logged out: ({request.user.username})")

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(f"User logout failed: {str(e)}")
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]
    pagination_class = CustomPaginationWithResult

    def get_queryset(self):
        return CustomUser.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        try:
            logger.info(f"User {request.user.email} viewed the list of users")
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error while fetching user list: {str(e)}")
            return Response({"error": "Could not retrieve users."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
