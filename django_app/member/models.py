from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

from research.models import Institution


class MyUserManager(BaseUserManager):
    def create_user(self, username, nickname, sex, date_of_birth, phone, institution, user_type='P', password=None):
        """
        아이디, 이니셜, 성별, 생년월일, 유저타입을 이용해 이용자를 생성한다.
        """
        if user_type == 'P':  # 유저타입이 환자인 경우
            user = self.model(
                username=username,
                nickname=nickname,
                sex=sex,
                date_of_birth=date_of_birth,
                phone=phone,
                institution=institution,
                user_type=user_type
            )
            user.set_password(password)
            user.save(using=self._db)
            return user
        elif user_type == 'R':  # 유저타입이 연구자인 경우
            user = self.model(
                username=username,
                nickname=nickname,
                institution=institution,
                user_type=user_type
            )
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self, username, nickname, user_type='D', password=None):
        """
        아이디, 닉네임, 비밀번호를 이용해 총괄운영자를 생성한다.
        """
        user = self.model(
            username=username,
            nickname=nickname,
            user_type=user_type
        )

        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(
        verbose_name='username',
        max_length=50,
        unique=True,
    )

    nickname = models.CharField(
        verbose_name='nickname',
        max_length=30,
        blank=True,
        null=True
    )

    CHOICES_SEX = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    sex = models.CharField(max_length=1, choices=CHOICES_SEX, blank=True, null=True)

    date_of_birth = models.DateField(
        verbose_name='date_of_birth',
        blank=True,
        null=True
    )

    phone = models.CharField(
        verbose_name='phone',
        max_length=11,
        blank=True,
        null=True
    )

    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True)

    fitbit = models.CharField(
        verbose_name='fitbit',
        max_length=100,
        blank=True,
        null=True
    )

    CHOICES_TYPE = (
        ('P', 'Patient'),
        ('R', 'Researcher'),
        ('D', 'Developer')
    )

    user_type = models.CharField(max_length=1, choices=CHOICES_TYPE)

    created = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nickname', 'user_type', ]

    def get_short_name(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        """
        이용자에게 특정 권한을 부여한다.
        """
        return True

    def has_module_perms(self, app_label):
        """
        이용자에게 앱을 볼 권한을 부여한다.
        """
        return True

    @property
    def is_staff(self):
        """
        스태프 권한을 가지고 있습니까?
        """
        return self.is_admin

    @property
    def is_superuser(self):
        """
        슈퍼유저 권한을 가지고 있습니까?
        """
        return self.is_admin

# class Membership(models.Model):
#     user = models.ForeignKey(MyUser, related_name='participants', on_delete=models.CASCADE)
#     institution = models.ForeignKey(Institution, related_name='institution', on_delete=models.CASCADE)
#     date_joined = models.DateField()
