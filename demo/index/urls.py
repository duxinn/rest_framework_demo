from django.conf.urls import url, include
from django.contrib import admin
from index import views
from rest_framework import routers


v1_d = {'get': 'list', 'post': 'create'}

v2_d = {'get': 'retrieve',
        'post': 'create',
        'delete': 'destroy',
        'put': 'update',
        'patch': 'partial_update',
        }

router = routers.DefaultRouter()
router.register(r'v2', views.V2)

urlpatterns = [
    # url('', views.User.as_view()),
    # url(r'^user$', views.User.as_view()),
    # url(r'^(?P<v>[v1|v2|v3]+)/order$', views.Order.as_view(), name='order'),
    # url(r'center$', views.Center.as_view()),
    # url(r'parser$', views.MyParser.as_view()),
    # url(r'customer$', views.Customer.as_view()),
    # url(r'^group/(?P<pk>\d+)$', views.Group.as_view(), name='ct'),
    # url(r'^usergroup$', views.UserGroup.as_view()),
    # url(r'^page$', views.Page.as_view()),
    # url(r'^v1$', views.V1.as_view()),
    #
    url(r'^v2\.(?P<form>\w+)$', views.V2.as_view(v1_d)),
    url(r'^v2$', views.V2.as_view(v1_d)),

    url(r'^v2/(?P<pk>\d+)$', views.V2.as_view(v2_d)),
    url(r'^v2/(?P<pk>\d+)\.(?P<form>\w+)$', views.V2.as_view(v2_d)),
    # 必须是pk
    # AssertionError: Expected view V2 to be called with a URL keyword argument named "pk".
    # Fix your URL conf, or set the `.lookup_field` attribute on the view correctly.
    url(r'^', include(router.urls))
]

