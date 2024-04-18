from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Bell, BellMovementRequest, Belltower, CustomUser, Temple

# class ChurchOperatorAdmin(admin.ModelAdmin):
#     list_display = ('username', 'is_key_keeper', 'is_bell_ringer')


class BellMovementRequestAdmin(admin.ModelAdmin):
    list_display = (
        "requester",
        "temple_from",
        "temple_to",
        "bell",
        "status",
        "created_at",
    )
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
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {"fields": ("username", "password")}),  # Include default fields
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "phone_number")},
        ),  # Include additional fields
        (
            "Permissions",
            {"fields": ("user_type", "is_key_keeper", "is_bell_ringer", "is_superuser")},
        ),  # Include custom fields
        (
            "Important dates",
            {"fields": ("last_login", "date_joined")},
        ),  # Include important dates
        ("Groups", {"fields": ("groups",)}),  # Include user groups
        ("Permissions", {"fields": ("user_permissions",)}),  # Include user permissions
    )
    # Add any other customizations as needed

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "user_type",
                    "is_key_keeper",
                    "is_bell_ringer",
                    "is_superuser",
                ),
            },
        ),
    )


# Регистрируем административный класс для модели CustomUser
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(BellMovementRequest, BellMovementRequestAdmin)
admin.site.register(Belltower)
admin.site.register(Bell)
admin.site.register(Temple)
