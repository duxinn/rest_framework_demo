import json
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions, serializers
from rest_framework.permissions import BasePermission
from rest_framework.authentication import BasicAuthentication
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.versioning import URLPathVersioning
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import CursorPagination

from index.myserializers import CustomerSerializer, \
    GroupSerializer, UserGroupSerializer, RoleSerializer
from index import models

ORDER_DICT = {
    1: {
        'name': "媳妇",
        'age': 18,
        'gender': '男',
        'content': '...'
    },
    2: {
        'name': "老狗",
        'age': 19,
        'gender': '男',
        'content': '...。。'
    },
}


class MyAuthentication(BasicAuthentication):
    def authenticate(self, request):
        token = request._request.GET.get('token')
        token_obj = models.UserInfo.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        # 在rest framework内部会将整个两个字段赋值给request，以供后续操作使用
        return token_obj, token_obj.user_name

    def authenticate_header(self, val):
        pass


class VIPPermission(BasePermission):
    message = "必须是VIP才能访问"

    def has_permission(self, request, view):
        if request.user.user_type != '3':
            return False
        return True


class MemberPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type not in ('2', '3'):
            return False
        return True


class User(APIView):

    def get(self, request, *args, **kwargs):
        return HttpResponse('get')

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': '登陆成功'}
        user = request._request.POST.get('username')
        pwd = request._request.POST.get('password')
        obj = models.UserInfo.objects.filter(user_name=user, password=pwd).first()
        if not obj:
            ret['code'] = 1001
            ret['msg'] = "用户名或密码错误"
        token = str(user) + '123'
        models.UserInfo.objects.filter(user_name=user).update(token=token)
        ret['token'] = token

        return JsonResponse(ret)

    def put(self, request, *args, **kwargs):
        return HttpResponse('更新Dog')

    def delete(self, request, *args, **kwargs):
        return HttpResponse('删除Dog')


class Order(APIView):
    authentication_classes = [MyAuthentication, ]
    permission_classes = [MemberPermission, ]
    versioning_class = URLPathVersioning

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': 'xxx', 'data': ORDER_DICT}
        self.dispatch
        # 获取具体的版本
        print('request.version', request.version)
        # 处理版本的对象
        print(request.versioning_scheme)
        # 生成版本
        print(request.versioning_scheme.reverse(viewname='order', request=request))
        print(request.versioning_scheme.reverse(viewname='order', request=request, kwargs={'v': 2}))
        '''
        request.version v2
        <rest_framework.versioning.URLPathVersioning object at 0x7fe2874c6160>
        http://localhost:9016/index/v2/order
        '''
        return JsonResponse(ret)


class Center(APIView):
    authentication_classes = [MyAuthentication, ]
    permission_classes = [VIPPermission, ]

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': 'xxx', 'data': ORDER_DICT}
        return JsonResponse(ret)

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': 'xxx', 'data': ORDER_DICT}
        return JsonResponse(ret)


class MyParser(APIView):
    parser_classes = [JSONParser, FormParser]

    def post(self, request, *args, **kwargs):
        print('request.data', request.data)
        # request.data {'name': '1', 'value': '2'}
        return HttpResponse('Parser post')


class Customer(APIView):
    def get(self, request, *args, **kwargs):
        # 方法一
        # cus = list(models.UserInfo.objects.all() \
        #            .values('user_type', 'user_name',
        #                    'address', 'token'))
        # # cus = json.dumps(cus)
        # # return HttpResponse(cus)
        # return JsonResponse(cus, safe=False)
        # # In order to allow non-dict objects to be serialized set the safe parameter to False.

        # 方法二
        cus = models.UserInfo.objects.all()
        ser = CustomerSerializer(instance=cus, many=True, context={'request': request})
        # ser = CustomerSerializer(instance=cus, many=False)
        ser = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ser)


class Group(APIView):
    def get(self, *args, **kwargs):
        pk = kwargs.get('pk')
        obj = models.MyUserGroup.objects.filter(pk=pk).first()
        ser = GroupSerializer(instance=obj, many=False)
        return JsonResponse(ser.data)


class UserGroup(APIView):
    def post(self, request, *args, **kwargs):
        # print(request.data)
        # < QueryDict: {'name': ['tom']} >
        # {'name': 'alerx'}

        ser = GroupSerializer(data=request.data)
        ser = UserGroupSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data['title'])
        else:
            print(ser.errors)
        return HttpResponse('UserGroup post')


class MyPageNumberPagination(PageNumberPagination):
    # 每页显示
    page_size = 2
    page_size_query_param = 'size'
    max_page_size = 10

    page_query_param = 'page'


class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 10


class MyCursorPagination(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 3
    ordering = 'id'
    page_size_query_param = 'size'

    max_page_size = 10


class Page(APIView):
    def get(self, request, *args, **kwargs):
        obj = models.Role.objects.all()
        # ser = RoleSerializer(instance=obj, many=True)
        # return Response(ser.data)

        # http://localhost:9016/index/page?page=1&size=4
        # pg = MyPageNumberPagination()

        # http://localhost:9016/index/page?offset=0&limit=2
        # pg = MyLimitOffsetPagination()

        pg = MyCursorPagination()

        page_role = pg.paginate_queryset(queryset=obj, request=request, view=self)
        # print(page_role)
        # [<Role: people>, <Role: doctor>]

        ser = RoleSerializer(instance=page_role, many=True)
        # return Response(ser.data)
        resp = pg.get_paginated_response(ser.data)
        return resp


from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import GenericAPIView


class V1(GenericAPIView):
    queryset = models.Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        # 获取数据
        role = self.get_queryset()
        # 分页
        page_role = self.paginate_queryset(role)
        # 序列化
        ser = self.get_serializer(instance=page_role, many=True)
        return Response(ser.data)


from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

class V2(ModelViewSet):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    queryset = models.Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = PageNumberPagination



