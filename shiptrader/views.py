from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import OrderingFilter

from shiptrader.models import Starship, Listing
from shiptrader.serializers import StarshipSerializer, ListingSerializer, ListingUpdateSerializer


class StarshipViewSet(mixins.ListModelMixin, GenericViewSet):
    """View that allows all starships to be listed"""

    queryset = Starship.objects.all()
    serializer_class = StarshipSerializer


class ListingViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    """View to create and list ship listings"""

    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('ship_type__starship_class',)
    ordering_fields = ('price', 'created')


class ListingActiveViewSet(mixins.UpdateModelMixin, GenericViewSet):
    """View to update listing to active / inactive"""

    queryset = Listing.objects.all()
    serializer_class = ListingUpdateSerializer
