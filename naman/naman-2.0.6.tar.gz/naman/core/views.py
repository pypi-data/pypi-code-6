from models import (
    Project,
    Machine,
    Iface,
    DNSZone,
    Environment,
    VLan,
    Role,
    OperatingSystem,
    MType,
    ExcludedIPRange,
    Service,
    VLanConfig,
    )
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponseBadRequest, Http404
from rest_framework import status
import simplejson
from serializers import (
    ProjectSerializer,
    MachineSerializer,
    IfaceSerializer,
    DNSZoneSerializer,
    EnvironmentSerializer,
    VLanSerializer,
    RoleSerializer,
    OperatingSystemSerializer,
    MTypeSerializer,
    ExcludedIPRangeSerializer,
    ServiceSerializer,
    VLanConfigSerializer)
    
        
class VLanConfigList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        vlanconfigs = VLanConfig.objects.all()
        serializer = VLanConfigSerializer(vlanconfigs, many=True)
        return Response(serializer.data)
    @csrf_exempt
    def post(self, request, format=None):
        try:
            serializer = VLanConfigSerializer(data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception, ex:
            
                return HttpResponseBadRequest(
                    content=simplejson.dumps({"errors": [str(ex), ]}),
                    content_type="application/json",
                )
    
class VLanConfigDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return VLanConfig.objects.get(pk=pk)
        except VLanConfig.DoesNotExist:
            raise Exception("Object not found")

    def get(self, request, pk, format=None):
        try:
            vlanconfig = self.get_object(pk)
            serializer = VLanConfigSerializer(vlanconfig)
            return Response(serializer.data)
        except Exception, ex:
            return HttpResponseBadRequest(
                    content=simplejson.dumps({"errors": [str(ex), ]}),
                    content_type="application/json",
                )
    def put(self, request, pk, format=None):
        try:
            vlanconfig = self.get_object(pk)
            serializer = VLanConfigSerializer(vlanconfig, data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception, ex:
            return HttpResponseBadRequest(
                    content=simplejson.dumps({"errors": [str(ex), ]}),
                    content_type="application/json",
                )
    def delete(self, request, pk, format=None):
        try:
            snippet = self.get_object(pk)
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception, ex:
            return HttpResponseBadRequest(
                    content=simplejson.dumps({"errors": [str(ex), ]}),
                    content_type="application/json",
                )
        
class MachineList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        machines = Machine.objects.all()
        serializer = MachineSerializer(machines, many=True)
        return Response(serializer.data)
    @csrf_exempt
    def post(self, request, format=None):
        try:
            serializer = MachineSerializer(data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception, ex:
            
                return HttpResponseBadRequest(
                    content=simplejson.dumps({"errors": [str(ex), ]}),
                    content_type="application/json",
                )
    
class MachineDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Machine.objects.get(pk=pk)
        except Machine.DoesNotExist:
            raise Http404(
                content=simplejson.dumps({"errors": ["Object not found", ]}),
                content_type="application/json",
                          )

    def get(self, request, pk, format=None):
        machine = self.get_object(pk)
        serializer = MachineSerializer(machine)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        machine = self.get_object(pk)
        serializer = MachineSerializer(machine, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        machine = self.get_object(pk)
        machine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class IfaceList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        machines = Iface.objects.all()[:3]
        serializer = IfaceSerializer(machines, many=True)
        return Response(serializer.data)
    @csrf_exempt
    def post(self, request, format=None):
        try:
            serializer = IfaceSerializer(data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception, ex:
            
                return HttpResponseBadRequest(
                    content=simplejson.dumps({"errors": [str(ex), ]}),
                    content_type="application/json",
                )
    
class IfaceDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Iface.objects.get(pk=pk)
        except Iface.DoesNotExist:
            raise Http404("Object not found")

    def get(self, request, pk, format=None):
        try:
            machine = self.get_object(pk)
            serializer = IfaceSerializer(machine)
            return Response(serializer.data)
        except Exception, ex:            
                return HttpResponseBadRequest(
                    content=simplejson.dumps({"errors": [str(ex), ]}),
                    content_type="application/json",
                )
            

    def put(self, request, pk, format=None):
        try:
            machine = self.get_object(pk)
            serializer = IfaceSerializer(machine, data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception, ex:            
                return HttpResponseBadRequest(
                    content=simplejson.dumps({"errors": [str(ex), ]}),
                    content_type="application/json",
                )

    def delete(self, request, pk, format=None):
        try:
            machine = self.get_object(pk)
            machine.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception, ex:            
                return HttpResponseBadRequest(
                    content=simplejson.dumps({"errors": [str(ex), ]}),
                    content_type="application/json",
                )
    
class ServiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ExcludedIPRangeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ExcludedIPRange.objects.all()
    serializer_class = ExcludedIPRangeSerializer


class OperatingSystemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = OperatingSystem.objects.all()
    serializer_class = OperatingSystemSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class MTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = MType.objects.all()
    serializer_class = MTypeSerializer


class DNSZoneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = DNSZone.objects.all()
    serializer_class = DNSZoneSerializer


class VLanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = VLan.objects.all()
    serializer_class = VLanSerializer


class EnvironmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

