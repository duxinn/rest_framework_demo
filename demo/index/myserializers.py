from rest_framework import serializers
from index import models


# class CustomerSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField(source='user_name')
#     xxx = serializers.CharField(source='user_type')
#     yyy = serializers.CharField(source='get_user_type_display')
#     gp = serializers.CharField(source='group.title')
#     # rls = serializers.CharField(source='role.all')
#     rls = serializers.SerializerMethodField()
#
#     def get_rls(self, row):
#         ret = []
#         for item in row.role.all():
#             ret.append({'id': item.id, 'title': item.role})
#         return ret


class CustomerSerializer(serializers.ModelSerializer):
    # 自定义字段
    rls = serializers.SerializerMethodField()
    group = serializers.HyperlinkedIdentityField(view_name='ct',
                                                 lookup_field='group_id',
                                                 lookup_url_kwarg='pk')

    class Meta:
        model = models.UserInfo
        # fields = '__all__'
        fields = ['id', 'user_name', 'address', 'phone_number', 'rls', 'group', 'role']
        # extra_kwargs = {'group': {'source': 'group.title'}}
        depth = 0

    # 自定义方法
    def get_rls(self, row):
        ret = []
        for item in row.role.all():
            ret.append({'id': item.id, 'title': item.role})
        return ret


class XXValidator(object):
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if not value.startswith(self.base):
            message = '标题必须以 %s 开头' % self.base
            raise serializers.ValidationError(message)

    def set_context(self, serializer_field):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # 执行验证之前调用,serializer_fields是当前字段对象
        pass


class GroupSerializer(serializers.ModelSerializer):
    serializers.Field
    title = serializers.CharField(error_messages={'required': '标题不能为空'}, validators=[XXValidator('老男人'), ])

    def validate_title(self, value):
        print(value)
        return value

    class Meta:
        model = models.MyUserGroup
        fields = '__all__'


class UserGroupSerializer(serializers.Serializer):
    title = serializers.CharField(error_messages={'required': '标题不能为空'}, validators=[XXValidator('老男人'), ])

    def validate_title(self, value):
        print(value)
        return value


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Role
        fields = '__all__'

