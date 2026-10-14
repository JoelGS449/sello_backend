from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'Sello — administración'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('cuentas.urls')),
]
