
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
