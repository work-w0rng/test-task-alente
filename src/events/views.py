from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from . import models, serializers, permissions


class EventViewSet(ModelViewSet):
    queryset = models.Event.objects.filter(start_date__gt=datetime.now())
    serializer_class = serializers.EventSerializer
    permission_classes = [permissions.IsAuthorOrReadOnly, permissions.IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_fields = ['name']
    search_fields = ['name', 'start_date', 'author__username']
    ordering_fields = ['name', 'start_date', 'author__username']

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()
