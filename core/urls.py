from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('api.user.urls')),
    path('', include('api.shapeteam.urls')),
    path('chats/', include('api.chat.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
