from rest_framework import serializers

from users.models import Users, Locations


class UsersCreateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        slug_field='name',
        queryset=Locations.objects.all())

    class Meta:
        model = Users
        exclude = ["id"]

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        users = Users.objects.create(**validated_data)

        for location in self._locations:
            location_obj, _ = Locations.objects.get_or_create(name=location)
            users.location.add(location_obj)
        users.set_password(validated_data["password"])
        users.save()
        return users


class UsersSerializer(serializers.ModelSerializer):
    total_ads = serializers.IntegerField()
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        slug_field='name',
        read_only=True)

    class Meta:
        model = Users
        fields = "__all__"


class LocationsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'
