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


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, tokens = serializer.save()
        print("User created successfully")

        return Response(
            {
                "data": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "phone_number": user.phone_number,
                        "role": user.role,
                        "refresh_token": tokens["refresh"],
                        "access_token": tokens["access"],
        
                }
            },
            status=status.HTTP_201_CREATED,
            
        )
    


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            user = self.get_user_from_request(request)  # Custom method to retrieve user
            tokens = response.data  # Contains refresh and access tokens
            print("Tokens generated successfully")
            print(request.data)
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

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPaginationWithResult

    def get_queryset(self):
        return CustomUser.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    


