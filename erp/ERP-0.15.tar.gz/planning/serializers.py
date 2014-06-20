__author__ = 'cltanuki'
from . import models
from rest_framework import serializers


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Task
        fields = '__all__'


class PrjSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__'