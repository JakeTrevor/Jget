from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class jgetUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username

    def __repr__(self) -> str:
        return f"<jgetUser {self.user.username}>"


class Package(models.Model):
    name = models.CharField(max_length=120, unique=True)
    authors = models.ManyToManyField(jgetUser)
    dependencies = models.ManyToManyField("Package", blank=True)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Package {self.name}>"


class File(models.Model):
    fileName = models.CharField(max_length=300)
    content = models.TextField(blank=True)
    package = models.ForeignKey(
        Package, related_name="files", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.fileName

    def __repr__(self) -> str:
        return f"<File {self.package} {self.fileName}>"
