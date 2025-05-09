from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentTeacher, Homework

print("Registering CustomUser in admin")  # Добавь эту строку для отладки


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "role",
        "teacher_code",
        "display_name",
        "is_staff",
    )
    list_filter = ("role", "is_staff")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("email", "display_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Custom fields", {"fields": ("role", "teacher_code")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "role",
                    "teacher_code",
                ),
            },
        ),
    )
    search_fields = ("username", "email")
    ordering = ("username",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentTeacher)
admin.site.register(Homework)
