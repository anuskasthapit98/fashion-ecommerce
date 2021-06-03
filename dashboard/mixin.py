
from django.shortcuts import  redirect
from django.contrib.auth.models import User, Group

class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_superuser:
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
