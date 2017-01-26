import inspect

from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets

from .generics.forms import DITHelpModelForm
from . import forms


class NonSuperuserReadOnlyAdmin(admin.ModelAdmin):
    """
    A custom ModelAdmin that fills a gap left by django.

    Inherit from this ModelAdmin if you want all is_staff Users to be able to
    VIEW a model and all of it's ModelAdmin's fields in the admin interface,
    but not be able to edit anything.  You need to still give the user the 'Can
    change' permission for the model for it to appear for them in the admin
    interface, but every field will appear read only.  Users that are marked
    is_superuser can still edit models as usual, as defined by permissions in
    the ModelAdmin
    """

    def has_add_permission(self, request, obj=None):
        # Can only add if user is superuser
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        # Can only delete if user is superuser
        return request.user.is_superuser

    def get_actions(self, request):
        # Remove the delete action (if present) if user is not superuser
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']

        return actions

    def get_readonly_fields(self, request, obj):
        # Make all fields readonly if the user is not a superuser
        if request.user.is_superuser:
            return self.readonly_fields

        return list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))


class DefaultAdmin(NonSuperuserReadOnlyAdmin):
    list_display = ('created', 'service', 'contact_name')
    list_filter = ('service',)


for name, form_cls in forms.__dict__.items():
    if isinstance(form_cls, type) and issubclass(form_cls, DITHelpModelForm) and form_cls is not DITHelpModelForm:
        model = form_cls.Meta.model
        admin_class = type('{0}Admin'.format(model.__name__), (DefaultAdmin,), {})
        if hasattr(form_cls, 'fieldsets'):
            admin_class.fieldsets = form_cls.fieldsets
        elif hasattr(form_cls, 'fields'):
            admin_class.fields = form_cls.fields
        admin.site.register(model, admin_class)
