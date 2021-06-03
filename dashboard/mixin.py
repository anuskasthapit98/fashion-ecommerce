
from django.shortcuts import redirect


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.groups.filter(name="Admin").exists():
            pass
        else:
            return redirect('/login/')
            # raise PermissionDenied

        return super().dispatch(request, *args, *kwargs)


class DeleteMixin():
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class NonDeletedItemMixin():
    def get_qyeryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
