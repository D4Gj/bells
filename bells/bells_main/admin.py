from django.contrib import admin

from .models import BellMovementRequest, CustomUser, Bell, Belltower, Temple


# class ChurchOperatorAdmin(admin.ModelAdmin):
#     list_display = ('username', 'is_key_keeper', 'is_bell_ringer')


# class BellMovementRequestAdmin(admin.ModelAdmin):
#     list_display = ("requester", "destination_church", "status", "created_at")
#     list_filter = ("status",)


# class BellMovementApprovalAdmin(admin.ModelAdmin):
#     list_display = ("request", "operator", "approved", "timestamp")
#     list_filter = ("approved",)


# class ReportAdmin(admin.ModelAdmin):
#     list_display = ("creator", "title", "created_at")


# Register your models with the custom admin classes
admin.site.register(CustomUser)
admin.site.register(BellMovementRequest)
admin.site.register(Belltower)
admin.site.register(Bell)
admin.site.register(Temple)
