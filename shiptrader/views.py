from rest_framework import serializers, viewsets

from shiptrader.models import Starship


class StarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Starship
        fields = '__all__'


class StarshipViewSet(viewsets.ReadOnlyModelViewSet):
    """View that allows all starships to be listed"""

    queryset = Starship.objects.all()
    serializer_class = StarshipSerializer
