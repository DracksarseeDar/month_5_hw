from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include 
from . import swagger
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/product/', include('product.urls')),
    path('api/v1/users/', include('users.urls'))
]

urlpatterns += swagger.urlpatterns