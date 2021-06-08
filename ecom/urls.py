from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
<<<<<<< HEAD
=======
from dashboard import views
>>>>>>> 903f3748b9dcc8be66a25fcb016adeb8a22ed150

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("dashboard.urls")),
<<<<<<< HEAD
    
=======
    path('', include("home.urls")),
    path('', include("api.urls")),

>>>>>>> 903f3748b9dcc8be66a25fcb016adeb8a22ed150
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
<<<<<<< HEAD
urlpatterns = format_suffix_patterns(urlpatterns)
=======
urlpatterns = format_suffix_patterns(urlpatterns)
>>>>>>> 903f3748b9dcc8be66a25fcb016adeb8a22ed150
