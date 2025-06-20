from django.contrib import admin
from django.urls import path, include
#Path to app
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('equipment_management.urls'))
]
