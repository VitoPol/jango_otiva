from django.db.models import Count, Q
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import Users, Locations
from users.serializers import UsersCreateSerializer, LocationsViewSerializer, UsersSerializer


class UsersListView(ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def get_queryset(self):
        return Users.objects.annotate(total_ads=Count('ads', filter=Q(ads__is_published=True)))


class UserDetailView(RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def get_queryset(self):
        return Users.objects.annotate(total_ads=Count('ads', filter=Q(ads__is_published=True)))


class UserCreateView(CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersCreateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersCreateSerializer


class LocationsViewSet(ModelViewSet):
    queryset = Locations.objects.all()
    serializer_class = LocationsViewSerializer
