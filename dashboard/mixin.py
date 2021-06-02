
from django.shortcuts import  redirect


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.groups.filter(name="Admin").exists():
            pass
        else:
            return redirect('/login/')
            # raise PermissionDenied

        return super().dispatch(request, *args, *kwargs)
