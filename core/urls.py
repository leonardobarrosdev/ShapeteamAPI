from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.user.urls')),
    path('', include('apps.shapeteam.urls')),
    # path('chats/', include('apps.chat.urls')),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

admin.site.site_header = "SHAPETEAM"
admin.site.site_title = _("SHAPETEAM Manegement")
admin.site.index_title = _("Administrative Area of SHAPETEAM")
