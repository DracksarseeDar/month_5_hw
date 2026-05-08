from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import (
    CategoryListSerializer, CategoryDetailSerializer, CategoryValidateSerializer,
    ProductListSerializer, ProductDetailSerializer, ProductValidateSerializer,
    ProductReviewSerializer,
    ReviewListSerializer, ReviewDetailSerializer, ReviewValidateSerializer
)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from common.permissions import IsOwner, IsModerator, IsAnonymous


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


# Category
class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryValidateSerializer
        else:
            return self.serializer_class

class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CategoryValidateSerializer
        else:
            return self.serializer_class
        

# Product
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    pagination_class = CustomPagination
    lookup_field = 'id'
    
    def get_permissions(self):
        if self.action == 'create':
           
            return [IsOwner()]
            
        elif self.action in ['list', 'retrieve']:
            return [(IsAnonymous | IsOwner | IsModerator)()]
            
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [(IsOwner | IsModerator)()]
            
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductValidateSerializer
        elif self.request.method == 'PUT':
            return ProductValidateSerializer
        else:
            if self.action == 'retrieve':
                return ProductDetailSerializer
            return self.serializer_class

# Review
class ReviewListAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewValidateSerializer
        else:
            return self.serializer_class

class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    lookup_field = 'id'

class ProductReviewListAPIView(ListAPIView):
    queryset = Product.objects.prefetch_related('reviews').all()
    serializer_class = ProductReviewSerializer
    pagination_class = CustomPagination