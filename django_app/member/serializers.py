from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

User = get_user_model()


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'password', 'nickname', 'sex', 'date_of_birth', 'institution', 'fitbit', 'user_type',
            'created', 'last_login')
        ordering = ('id',)


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            )
        ]
    )

    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = (
            'id', 'username', 'password', 'nickname', 'sex', 'date_of_birth', 'institution', 'user_type')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
            sex=validated_data['sex'],
            date_of_birth=validated_data['date_of_birth'],
            institution=validated_data['institution'],
            user_type=validated_data['user_type'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
        else:
            msg = _('유저명 혹은 비밀번호가 맞지 않습니다.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs
