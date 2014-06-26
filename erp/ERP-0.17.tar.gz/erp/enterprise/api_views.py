from . import serializers, models

__author__ = 'cltanuki'
from rest_framework import generics


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
    model = models.CorpObject
    serializer_class = serializers.ObjSerializer