from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from api.models import Package


class UserRelatedField(serializers.RelatedField):
    queryset = User.objects.all()

    def to_representation(self, value) -> str:
        return str(value)

    def to_internal_value(self, data) -> User:
        return User.objects.get(username=data)


class PackageRelatedField(serializers.RelatedField):
    queryset = Package.objects.all()

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return Package.objects.get(name=data)


class PackageSerializer(serializers.ModelSerializer):
    authors = UserRelatedField(many=True)
    dependencies = PackageRelatedField(many=True)

    class Meta:
        model = Package
        fields = [
            "name", "dependencies", "files"
        ]
        depth = 1

    def create(self, validated_data):
        dependencies = validated_data.pop("dependencies", [])

        package = Package(**validated_data)
        package.save()
        package.dependencies.set(dependencies)
        package.save()
        return package

    def update(self, instance: Package, validated_data):
        user = validated_data.pop("creator")
        dependencies = validated_data.pop("dependencies", [])

        if not instance.is_owner(user):
            raise PermissionDenied

        instance.files = validated_data.pop("files")
        instance.dependencies.set(dependencies)
        instance.save()

        return instance
