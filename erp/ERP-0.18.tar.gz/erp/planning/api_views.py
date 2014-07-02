from . import models, serializers

__author__ = 'cltanuki'
from rest_framework import generics


class OwnedTasksViewSet(generics.ListAPIView):
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return models.Task.objects.filter(owner=user)


class OwnedPrjViewSet(generics.ListAPIView):
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return models.Project.objects.filter(owner=user)


class TaskPerformerViewSet(generics.ListAPIView):
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return models.Task.objects.filter(performer=user)


class PrjPerformerViewSet(generics.ListAPIView):
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return models.Project.objects.filter(performer=user)


class TaskJoinedViewSet(generics.ListAPIView):
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        return self.request.user.task_assigned_users.all()


class PrjJoinedViewSet(generics.ListAPIView):
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        return self.request.user.prj_assigned_users.all()


class PublicTasksViewSet(generics.ListAPIView):
    queryset = models.Task.objects.filter(public=True)
    serializer_class = serializers.TaskSerializer


class PublicPrjViewSet(generics.ListAPIView):
    queryset = models.Project.objects.filter(public=True)
    serializer_class = serializers.TaskSerializer


class PrjTaskViewSet(generics.ListAPIView):
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        prj = self.request.QUERY_PARAMS['prj_id']
        return models.Task.objects.filter(prj=prj)


class TaskDetailView(generics.RetrieveAPIView):
    models = models.Task
    serializer_class = serializers.TaskSerializer


class PrjDetailView(generics.RetrieveAPIView):
    models = models.Task
    serializer_class = serializers.PrjSerializer