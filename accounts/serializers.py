from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'full_name', 'phone_number', 'password', 'role' , 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        request = self.context.get('request')
        role = data.get('role', 'user')
        # if role != 'user' and not (request and request.user.is_authenticated and request.user.role == 'admin'):
        #     raise serializers.ValidationError({"role": "Only admins can set this role."})
        return data

    def create(self, validated_data):
        role = validated_data.pop('role', 'user')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            full_name=validated_data['full_name'],
            phone_number=validated_data.get('phone_number'),
            is_active = validated_data.get('is_active', True),
            password=validated_data['password'],
            role=role
        )
        # Generate token for the new user
        refresh = RefreshToken.for_user(user)
        token_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        # Return a tuple (user, token)
        return user, token_data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['full_name'] = user.full_name
        token['phone_number'] = user.phone_number
        
        return token

        # Set the password
        user.set_password(validated_data['password'])
        user.save()

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'full_name', 'phone_number', 'role']

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', {})
        request = context.get('request')
        # if request and request.user.role != 'admin':
        #     self.fields['role'].read_only = True


