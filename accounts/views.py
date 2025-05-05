from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializers import *
from forensicapp.pagination import  CustomPaginationWithResult
import logging


logger = logging.getLogger('accounts')  # logger defined in settings


class UserManagementView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request, *args, **kwargs):
        """Create a new user"""
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user, tokens = serializer.save()  # Create user and generate tokens

                logger.info(f"New user registered: {user.email} ({user.username})")

                return Response({
                    "data": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "full_name": user.full_name,
                        "phone_number": user.phone_number,
                        "role": user.role,
                        "refresh_token": tokens["refresh"],
                        "access_token": tokens["access"],
                    }
                }, status=status.HTTP_201_CREATED)

            logger.error(f"User registration failed: {serializer.errors}")
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error during user creation: {str(e)}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, *args, **kwargs):
        """Update an existing user and regenerate tokens if updated"""
        try:
            user = CustomUser.objects.filter(id=pk).first()

            if not user:
                logger.error(f"Update failed: User with ID {pk} not found")
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            # Serialize the incoming data (use the same serializer that was used to create the user)
            serializer = UserSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                # Save the updated user details
                serializer.save()

                # Regenerate the tokens
                refresh_token = RefreshToken.for_user(user)
                new_access_token = str(refresh_token.access_token)
                new_refresh_token = str(refresh_token)

                logger.info(f"User {user.username} (ID: {pk}) updated successfully, tokens regenerated.")

                return Response({
                    "message": "User updated successfully",
                    "data": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "full_name": user.full_name,
                        "phone_number": user.phone_number,
                        "role": user.role,
                        "refresh_token":new_refresh_token,
                        "access_token": new_access_token,
                    }
                }, status=status.HTTP_200_OK)

            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error during user update: {str(e)}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk, *args, **kwargs):
        try:
            user = CustomUser.objects.filter(id=pk).first()

            if not user:
                logger.error(f"Delete failed: User with ID {pk} not found")
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            # blacklist all refresh tokens for the user
            token = RefreshToken.objects.filter(user=user)
            token.blacklist()  # Blacklist the token

            # Delete the user
            user.delete()
            logger.info(f"User {user.username} (ID: {pk}) deleted successfully")

            return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Unexpected error during user deletion: {str(e)}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                        "full_name":user.full_name,
                        "phone_number": user.phone_number,
                        "role":user.role,
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
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                logger.error("Logout failed: Refresh token missing")
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Blacklist the refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()

                # Deactivate the user once the token is blacklisted
                request.user.is_active = False
                request.user.save()

                logger.info(f"User logged out successfully and deactivated: {request.user.username}")
                return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)

            except TokenError:
                logger.error("Logout failed: Invalid or expired refresh token")
                return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Unexpected error during logout: {str(e)}")
            return Response({"error": f"An unexpected error occurred:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPaginationWithResult

    def get_queryset(self):
        return CustomUser.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        try:
            logger.info(f"User list accessed")
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error while fetching user list: {str(e)}")
            return Response({"error": "Could not retrieve users."}, status=500)

class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            user_id = request.data.get("id")
            old_password = request.data.get("old_password")
            new_password = request.data.get("new_password")

            if not user_id or not old_password or not new_password:
                logger.warning(f"[{user.username}] Password change failed: Missing fields")
                return Response({"error": "id, old_password, and new_password are required."}, status=status.HTTP_400_BAD_REQUEST)

            if str(user.id) != str(user_id):
                logger.warning(f"[{user.username}] ID mismatch during password change attempt")
                return Response({"error": "You are not authorized to change this user's password."}, status=status.HTTP_403_FORBIDDEN)

            if not user.check_password(old_password):
                logger.warning(f"[{user.username}] Incorrect old password")
                return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            logger.info(f"[{user.username}] Password changed successfully")

            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"[{request.user.username}] Unexpected error during password change: {str(e)}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
