from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import UserSerializer, SignUpSerializer, SignInSerializer, TokenSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class SignUpViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = SignInSerializer(data=request.data)
        token_model = Token

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, _ = token_model.objects.get_or_create(user=user)
            serializer_token = TokenSerializer(instance=Token)
            return Response(serializer_token.data, status=status.HTTP_200_OK)


class SignOutViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        try:
            request.auth.delete()
        except (AttributeError, ObjectDoesNotExist):
            return Response({'detail': 'Token Does Not Exist.'}, status=status.HTTP_400_BAD_REQUEST)

        logout(request)
        return Response({'detail': 'Sign-Out Success!'}, status=status.HTTP_200_OK)
