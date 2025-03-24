from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserManagementView , LogoutView , MyObtainTokenPairView , UserListView 


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='login'),
    path('register/', UserManagementView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('register/<int:pk>/', UserManagementView.as_view(), name='user-delete'),


]

