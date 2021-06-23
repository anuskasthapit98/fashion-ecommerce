from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.views.generic.base import TemplateView

from dashboard.models import CategoryType


class StaffRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff and user.is_active:
            pass
        else:
            return redirect('/login/')
        return super().dispatch(request, *args, *kwargs)


class CustomLoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):

        user = request.user
        if user.is_superuser or (user.is_staff and user.is_active):
            pass
        else:
            return redirect('dashboard:login')
        return super().dispatch(request, *args, **kwargs)


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


class SidebarMixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_categories'] = CategoryType.objects.filter(
            deleted_at__isnull=True)

        return context
