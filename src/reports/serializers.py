from reports.models import Other
from reports.models import Vul
from reports.models import Mal

from rest_framework import serializers

class OtherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Other
        fields = ['ip', 'rede', 'data_1', 'data_2', 'count']

class VulSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vul
        fields = ['ip', 'port', 'rede', 'data_1', 'data_2', 'count']

class MalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mal
        fields = ['ip', 'rede', 'data_1', 'data_2', 'count']
