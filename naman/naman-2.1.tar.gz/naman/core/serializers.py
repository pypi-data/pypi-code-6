from models import *

from rest_framework import serializers


class ExcludedIPRangeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExcludedIPRange
        fields = ('first', 'last', 'vlan', 'id', )


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Service
        fields = ('name', 'description', 'iface', )


class DNSZoneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DNSZone
        fields = ('name', 'id', )


class VLanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VLan
        fields = ('name', 'ip', 'gw', 'mask', 'tag', 'id', 'management_purpose', 'provisioning_purpose', )
        lookup_field = "code"


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = ('code', 'description', 'id', )


class OperatingSystemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OperatingSystem
        fields = ('code', 'description', 'id', )


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('name', 'code', 'machines', 'id', )


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ('code', 'description', 'id', )


class MTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MType


class MachineSerializer(serializers.HyperlinkedModelSerializer):
    interfaces = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                 view_name='iface-detail')

    fqdn = serializers.Field(source="fqdn")
    class Meta:
        model = Machine
        fields = (
            "hostname",
            "virtual",
            'environment',
            'role',
            'operating_system',
            "dns_zone",
            "project",
            "mtype",
            "interfaces",
            "id",
            "fqdn",)


class IfaceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Iface
        fields = (
            'name',
            'ip',
            'vlan',
            'gw',
            'mask',
            'machines',
            'id',
            'virtual',
            'nat',
            'mac',
            "dhcp",)


class VLanConfigSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VLanConfig

