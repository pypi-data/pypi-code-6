__author__ = 'cltanuki'
from . import models, serializers
from rest_framework import viewsets, generics


class UserViewSet(generics.ListAPIView):
    model = models.CorpUser
    serializer_class = serializers.UserSerializer


class GroupViewSet(generics.ListAPIView):
    model = models.CorpUnit
    serializer_class = serializers.GroupSerializer


class ObjViewSet(generics.ListAPIView):
    model = models.CorpObject
    serializer_class = serializers.ObjSerializer


class UserView(generics.RetrieveAPIView):
    model = models.CorpUser
    serializer_class = serializers.UserSerializer


class GroupView(generics.RetrieveAPIView):
    model = models.CorpUnit
    serializer_class = serializers.GroupSerializer


class ObjView(generics.RetrieveAPIView):
    moodel = models.CorpObject
    serializer_class = serializers.ObjSerializer