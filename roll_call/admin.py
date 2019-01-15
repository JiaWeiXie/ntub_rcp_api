from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *


admin.site.register(Beacon)
# admin.site.register(RollCallCheck)
# admin.site.register(RollCallRecord)
admin.site.register(RollCallCheckHistory)


class RollCallCheckResource(resources.ModelResource):
    class Meta:
        model = RollCallCheck


@admin.register(RollCallCheck)
class RollCallCheckAdmin(ImportExportModelAdmin):
    resource_class = RollCallCheckResource


class RollCallRecordResource(resources.ModelResource):
    class Meta:
        model = RollCallRecord


@admin.register(RollCallRecord)
class RollCallRecordAdmin(ImportExportModelAdmin):
    resource_class = RollCallRecordResource
