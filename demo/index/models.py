from django.db import models

# Create your models here.


class UserInfo(models.Model):
    user_type = (
        ('1', '普通用户'),
        ('2', '会员用户'),
        ('3', 'VIP用户'),
    )
    user_type = models.CharField(choices=user_type, max_length=32)
    user_name = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    token = models.CharField(max_length=64, default='123')
    address = models.CharField(max_length=64, default='address')
    phone_number = models.IntegerField(default=123456)
    role = models.ManyToManyField(to='Role', default=1)
    group = models.ForeignKey('MyUserGroup', on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = 'user_info'

        verbose_name = '客户'

        verbose_name_plural = verbose_name


class Role(models.Model):
    role = models.CharField(max_length=64, default='people')

    def __str__(self):
        return self.role

    class Meta:
        db_table = 'role'
        verbose_name = '角色'
        verbose_name_plural = verbose_name


class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo', on_delete=models.SET_DEFAULT, default='1')
    token = models.CharField(max_length=64)

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'user_token'
        verbose_name = '用户token'
        verbose_name_plural = verbose_name


class MyUserGroup(models.Model):
    title = models.CharField(max_length=32, default='a group')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'my_user_group'
        verbose_name = '用户组'
        verbose_name_plural = verbose_name


