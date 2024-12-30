from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (

    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/', include('books.urls')),
    path('api/', include('users.urls'))
]

if settings.DEVEL:
    urlpatterns += static('/media', document_root=settings.MEDIA_ROOT)