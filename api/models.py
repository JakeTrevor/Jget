from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Package(models.Model):
    name = models.CharField(max_length=120, unique=True)
    creator = models.ForeignKey(
        User, related_name="packages", on_delete=models.CASCADE)
    authors = models.ManyToManyField(User, related_name="collaborations")
    dependencies = models.ManyToManyField("Package", blank=True)

    views = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Package {self.name}>"

    def isAuthor(self, user: User):
        return (user in self.authors.all()) or (user == self.creator)


class File(models.Model):
    fileName = models.CharField(max_length=300)
    content = models.TextField(blank=True)
    package = models.ForeignKey(
        Package, related_name="files", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("package", "fileName")

    def __str__(self) -> str:
        return self.fileName

    def __repr__(self) -> str:
        return f"<File {self.package} {self.fileName}>"
