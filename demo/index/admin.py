from django.contrib import admin
from django.utils.html import format_html

from index.models import UserInfo
from index.models import MyUserGroup
from index.models import Role
from index.models import UserToken

# Register your models here.


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user_type', 'user_name', 'password', 'token', 'address',
                    'phone_number', 'show_tags', 'group')

    '''展示tags'''

    def show_tags(self, obj):
        tag_list = []
        tags = obj.role.all()
        if tags:
            for tag in tags:
                tag_list.append(tag.role)
            return ','.join(tag_list)
        else:
            return format_html(
                '<span style="color:red;">用户{}无角色</span>',
                obj.id, )

    '''设置表头'''
    show_tags.short_description = '角色'  # 设置表头


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(MyUserGroup)
admin.site.register(Role)
admin.site.register(UserToken)

