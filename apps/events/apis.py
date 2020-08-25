from rest_framework import viewsets

from events.models import Events
from events.serializer import EventsSerializer


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
