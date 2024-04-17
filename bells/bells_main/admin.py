from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BellMovementRequest, CustomUser, Bell, Belltower, Temple


# class ChurchOperatorAdmin(admin.ModelAdmin):
#     list_display = ('username', 'is_key_keeper', 'is_bell_ringer')


class BellMovementRequestAdmin(admin.ModelAdmin):
    list_display = ("requester", "destination_church", "status", "created_at")
    list_filter = ("status",)

# class CustomUserAdmin(admin.ModelAdmin):
#     # Переопределяем методы, чтобы модераторы не имели доступа к пользователям
#     def has_module_permission(self, request):
#         return False
    
#     def has_view_permission(self, request, obj=None):
#         return False
    
#     def has_add_permission(self, request):
#         return False
    
#     def has_change_permission(self, request, obj=None):
#         return False
    
#     def has_delete_permission(self, request, obj=None):
#         return False

# Регистрируем административный класс для модели CustomUser
# admin.site.register(CustomUser, CustomUserAdmin)
#TODO: передалать модельку, только админ может заводить новых пользователей
admin.site.register(CustomUser)
admin.site.register(BellMovementRequest, BellMovementRequestAdmin)
admin.site.register(Belltower)
admin.site.register(Bell)
admin.site.register(Temple)
