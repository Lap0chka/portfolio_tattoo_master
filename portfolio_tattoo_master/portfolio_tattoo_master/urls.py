

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rosetta/", include("rosetta.urls")),
    path('captcha/', include('captcha.urls')),
] + i18n_patterns(
    path("i18n/", include("django.conf.urls.i18n")),
    path('', include('portfolio.urls')),
    path('blog/', include('blog.urls')),


)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
