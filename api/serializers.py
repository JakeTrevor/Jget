from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from api.models import File, Package


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


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ["fileName", "content"]


class PackageSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True)
    authors = UserRelatedField(many=True)
    dependencies = PackageRelatedField(many=True)

    class Meta:
        model = Package
        fields = [
            "name", "dependencies", "files", "authors"
        ]
        depth = 1

    def create(self, validated_data):
        files = validated_data.pop("files", [])
        authors = validated_data.pop("authors", [])
        dependencies = validated_data.pop("dependencies", [])
        package = Package(**validated_data)
        package.save()
        package.authors.set(authors)
        package.dependencies.set(dependencies)
        package.save()
        for f in files:
            dbFile = File(package=package, **f)
            dbFile.save()
        return package

    def __init__(self, *args, **kwargs):
        exclude = kwargs.pop('exclude', None)
        super().__init__(*args, **kwargs)

        if exclude is not None:
            # Drop any fields that are not specified in the `fields` argument.
            disallowed = set(exclude)
            for field_name in disallowed:
                self.fields.pop(field_name)
