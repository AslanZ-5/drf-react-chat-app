from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.shortcuts import get_object_or_404


def service_icon_upload_path(instance, filename):
    return f"service/{instance.name}/service_icons/{filename}"


def service_banner_upload_path(instance, filename):
    return f"service/{instance.name}/service_banner/{filename}"


def category_icon_upload_path(instance, filename):
    return f"category/{instance.name}/category_icon/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(upload_to=category_icon_upload_path, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.id:
            existing_cat = get_object_or_404(Category, id=self.id)
            if existing_cat.icon != self.icon:
                existing_cat.icon.delete(save=False)
        super(Category, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="service.Category")
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="server_category"
    )
    descriptions = models.CharField(max_length=250, null=True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner"
    )
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="channel_service"
    )
    banner = models.ImageField(
        upload_to=service_banner_upload_path, null=True, blank=True
    )
    icon = models.ImageField(upload_to=service_icon_upload_path, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        if self.id:
            existing = get_object_or_404(Service, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
            if existing.banner != self.icon:
                existing.banner.delete(save=False)
        super(Channel, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="service.Channel")
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon" or field.name == "banner":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self):
        return self.name
