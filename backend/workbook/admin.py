from django.contrib import admin

from workbook.models import Attempt, CostEntry, LabCheckpoint, SettingBlob

admin.site.register(Attempt)
admin.site.register(LabCheckpoint)
admin.site.register(CostEntry)
admin.site.register(SettingBlob)
