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


# todo improve serializer
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
            File(package=package, **f).save()
        return package

    def update(self, instance: Package, validated_data):
        user = validated_data.pop("creator")
        files = validated_data.pop("files", [])
        authors = validated_data.pop("authors", [])
        dependencies = validated_data.pop("dependencies", [])

        if not instance.isAuthor(user):
            raise PermissionDenied

        instance.authors.set(authors)
        instance.dependencies.set(dependencies)
        instance.save()

        for f in files:
            File.objects.update_or_create(package=instance, **f)

        fnames = [each["fileName"] for each in files]

        to_delete = File.objects.filter(
            package=instance).exclude(fileName__in=fnames)
        [each.delete() for each in to_delete]

        return instance

    def __init__(self, *args, **kwargs):
        exclude = kwargs.pop('exclude', None)
        super().__init__(*args, **kwargs)

        if exclude is not None:
            # Drop any fields that are not specified in the `fields` argument.
            disallowed = set(exclude)
            for field_name in disallowed:
                self.fields.pop(field_name)
