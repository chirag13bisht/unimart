from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, waitlist

class UserAdmin(admin.ModelAdmin):
    add_form_template = "admin/auth/user/add_form.html"
    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "university")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    ordering = ("username",)

@admin.action(description="Approve selected users")
def set_approved(self):
    queryset = self.get_queryset()
    for user in queryset:
        user.college = user.waitlist.university
        user.save()
        user.waitlist.delete()

@admin.action(description="Reject selected users")
def set_rejected(self):
    queryset = self.get_queryset()
    for user in queryset:
        user.waitlist.delete()


class waitlistAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "university", "enrollment_number")
    ordering = ("name",)
    actions = [set_approved, set_rejected]


admin.site.register(User, UserAdmin)
