from rest_framework import viewsets
from addresses.models import Province, City
from addresses.serializers import ProvinceSerializer, CitySerializer


class ProvinceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for the Province resouce
    """
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for the City resource
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
