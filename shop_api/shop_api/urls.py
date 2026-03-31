from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from product import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/category/', views.category_list_api_view),
    path('api/v1/category/<int:id>/', views.category_detail_api_view),
    path('api/v1/product/', views.product_list_api_view),
    path('api/v1/product/<int:id>/', views.product_detail_api_view),
    path('api/v1/review/', views.review_list_api_view),
    path('api/v1/review/<int:id>/', views.review_detail_api_view),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
