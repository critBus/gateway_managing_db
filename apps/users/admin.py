from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.utils.safestring import mark_safe

from apps.users.models import User

admin.site.unregister(Group)


class ManyToManyWidget(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        if value is not None:
            value = [str(v) for v in value]
        else:
            value = []

        output = value

        return mark_safe("<br/>".join(output))


@admin.register(Group)
class CustomRoleAdmin(admin.ModelAdmin):
    readonly_fields = ("name",)
    filter_horizontal = ("permissions",)

    list_display = (
        "id",
        "name",
    )
    search_fields = (
        "id",
        "name",
    )
    ordering = (
        "-id",
        "name",
    )
    list_display_links = (
        "id",
        "name",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        # Check if the user has read-only permissions
        # print("hace la pregunta")
        # if not self.has_change_permission(request,obj):
        if obj and "adminform" in context:
            adminform = context["adminform"]
            if adminform.readonly_fields and "permissions" in adminform.readonly_fields:
                # print("pasa por aqui")
                adminform.readonly_fields.remove("permissions")
                adminform.form.fields["permissions"] = forms.CharField(
                    label="Permisos",
                    initial=obj.permissions.all(),
                    widget=ManyToManyWidget(),
                )

        return super().render_change_form(request, context, add, change, form_url, obj)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    def grupos(self, obj):
        nombres = [v.name for v in Group.objects.filter(permissions=obj)]
        return mark_safe("<br>\n".join(nombres))

    list_display = ("id", "name", "grupos")
    search_fields = (
        "id",
        "name",
    )
    list_filter = ("group__name",)
    ordering = (
        "-id",
        "name",
    )
    list_display_links = (
        "id",
        "name",
    )
    fieldsets = ((None, {"fields": ("name",)}),)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
    )
    list_display = ("username", "email", "first_name", "is_staff")
    search_fields = ("username", "first_name", "last_name", "email")


admin.site.register(User, MyUserAdmin)
