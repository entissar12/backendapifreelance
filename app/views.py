from rest_framework import viewsets
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ('category', 'location', 'employer')
    ordering_fields = ('publish_date', 'budget')

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user.profile)


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('freelancer',)

    def perform_create(self, serializer):
        serializer.save(freelancer=self.request.user.profile)


class TokenViewSet(viewsets.ModelViewSet):
    queryset = ResetToken.objects.all()
    serializer_class = ResetTokenSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('token_reset', 'created',)


