from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shapeteam/', include('api.shapeteam.urls')),
    path('user/', include('api.user.urls')),
    path('chat/', include('api.chat.urls')),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
