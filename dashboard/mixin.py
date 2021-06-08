from django.core.exceptions import PermissionDenied
from django.shortcuts import  redirect
from django.contrib.auth.models import User, Group




class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_superuser:
        # if user.is_authenticated and user.groups.filter(name="Admin").exists():
            pass
        else:
            return redirect('/login/')
          

        return super().dispatch(request, *args, *kwargs)


class DeleteMixin(object):
    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class NonDeletedItemMixin(object):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class SuperAdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            pass
        else:
            raise PermissionDenied

        return super().dispatch(request, *args, *kwargs)


class QuerysetMixin(object):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)