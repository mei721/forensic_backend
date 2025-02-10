from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView , LogoutView , MyObtainTokenPairView , UserListView


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserListView.as_view(), name='user-list'),

]

