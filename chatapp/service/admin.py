from django.contrib import admin

from .models import Category, Channel, Service

admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Channel)
# Register your models here.
