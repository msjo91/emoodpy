"""
생성한 커스텀 유저 모델을 admin 페이지에 반영한다.
"""
from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """
    필수 필드와 비밀번호를 이용해 이용자를 생성하는 모델폼.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'username', 'nickname', 'sex', 'date_of_birth', 'institution', 'fitbit', 'is_active',
            'is_admin')

    def clean_password2(self):
        """
        두 비밀번호가 같은지 확인한다.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('재입력한 비밀번호가 다릅니다.')
        return password2

    def save(self, commit=True):
        """
        비밀번호를 해쉬로 변환해 저장한다.
        """
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    이용자 업데이트를 위한 모델폼.
    비밀번호는 해쉬된 값을 보여준다.
    """
    password = ReadOnlyPasswordHashField()

    def clean_password(self):
        """
        이용자의 입력과 관계없이 초기값을 불러온다.
        """
        return self.initial['password']


class UserAdmin(BaseUserAdmin):
    """
    이용자 인스턴스의 추가, 수정을 위한 폼.
    """
    form = UserChangeForm
    add_form = UserCreationForm

    # 기본 UserAdmin을 MyUser 모델의 필드로 덮어쓴다.
    list_display = (
        'id', 'username', 'nickname', 'sex', 'institution', 'user_type', 'created', 'last_login', 'is_active',
        'is_admin')
    list_filter = ('sex', 'institution', 'user_type', 'is_active', 'is_admin')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Info', {'fields': (
            'nickname', 'sex', 'date_of_birth', 'phone', 'institution', 'fitbit', 'last_login', 'is_active')}),
        ('Permissions', {'fields': ('user_type', 'is_admin',)}),
    )

    # 이용자 생성시 get_fieldsets를 덮어쓴다.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'nickname', 'sex', 'date_of_birth', 'phone', 'institution', 'user_type', 'fitbit',
                'password1',
                'password2'),
        }),
    )
    search_fields = ('id', 'username', 'sex', 'institution', 'user_type')
    ordering = ('id',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
