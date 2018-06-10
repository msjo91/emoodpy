from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class SignInForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=50)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    nickname = forms.CharField(max_length=30)
    sex = forms.ChoiceField(
        choices=User.CHOICES_SEX,
        widget=forms.Select()
    )

    def clean_username(self):
        """
        아이디 검증 로직
        """
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('이미 사용 중인 유저명입니다.')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        validate_password(password2)
        if password1 != password2:
            raise forms.ValidationError('두 비밀번호가 다릅니다.')
        return password2

    def create_user(self):
        username = self.cleaned_data['username']
        password2 = self.cleaned_data['password2']
        nickname = self.cleaned_data['nickname']
        sex = self.cleaned_data['gender']
        date_of_birth = self.cleaned_data['date_of_birth']
        institution = self.cleaned_data['institution']
        user_type = self.cleaned_data['user_type']

        user = User.objects.create_user(
            username=username,
            password=password2,
            nickname=nickname,
            institution=institution,
            user_type=user_type
        )

        user.sex = sex
        user.date_of_birth = date_of_birth
        user.save()
        return user


class SignUpModelForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'nickname',
            'institution',
            'user_type'
        )


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'nickname',
            'password',
            'institution',
            'sex',
            'date_of_birth'
        )
