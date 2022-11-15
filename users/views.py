import json

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ViewSet, ModelViewSet

from ads.models import Ads
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
