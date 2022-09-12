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
            "name", "dependencies", "files", "authors"
        ]
        depth = 1

    def create(self, validated_data):
        authors = validated_data.pop("authors", [])
        dependencies = validated_data.pop("dependencies", [])

        package = Package(**validated_data)
        package.save()
        package.authors.set(authors)
        package.dependencies.set(dependencies)
        package.save()
        return package

    def update(self, instance: Package, validated_data):
        user = validated_data.pop("creator")
        authors = validated_data.pop("authors", [])
        dependencies = validated_data.pop("dependencies", [])

        if not instance.is_owner(user):
            raise PermissionDenied

        instance.files = validated_data.pop("files")
        instance.authors.set(authors)
        instance.dependencies.set(dependencies)
        instance.save()

        return instance

    def __init__(self, *args, **kwargs):
        exclude = kwargs.pop('exclude', None)
        super().__init__(*args, **kwargs)

        if exclude is not None:
            # Drop any fields that are not specified in the `fields` argument.
            disallowed = set(exclude)
            for field_name in disallowed:
                self.fields.pop(field_name)
