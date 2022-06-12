from dataclasses import field, fields
from struct import pack
from rest_framework import serializers
from api.models import File, Package, jgetUser


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ["fileName", "content"]


class PackageSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True)

    class Meta:
        model = Package
        fields = [
            "name", "dependencies", "files"
        ]
        depth = 1

    def create(self, validated_data):
        files = validated_data.pop("files", [])
        package = Package(**validated_data)
        package.save()
        for f in files:
            dbFile = File(package=package, **f)
            dbFile.save()
        return package
