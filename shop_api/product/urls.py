from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListAPIView.as_view()),
    path('categories/<int:id>/', views.CategoryDetailAPIView.as_view()),
    path('reviews/', views.ReviewListAPIView.as_view()),
    path('reviews/<int:id>/', views.ReviewDetailAPIView.as_view()),
    path('products/reviews/', views.ProductReviewListAPIView.as_view()),
    path('products/', views.ProductViewSet.as_view({
        'get': 'list', 'post': 'create'
    })),
    path('products/<int:id>/', views.ProductViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    })),
]