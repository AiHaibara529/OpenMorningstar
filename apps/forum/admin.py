from django.contrib import admin
from django.db import models
# https://django-import-export.readthedocs.io/en/latest/getting_started.html
from import_export import resources
from import_export.formats import base_formats
from import_export.fields import Field
from import_export.admin import ImportExportModelAdmin, ImportMixin, ExportMixin, ImportExportActionModelAdmin
from .models import Room, Topic, Message


@admin.register(Room)
class RoomAdmin(ImportExportModelAdmin):
    pass


@admin.register(Topic)
class TopicAdmin(ImportExportModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(ImportExportModelAdmin):
    pass
