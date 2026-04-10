from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import (
    CategoryListSerializer, CategoryDetailSerializer,
    ProductListSerializer, ProductDetailSerializer,
    ReviewListSerializer, ReviewDetailSerializer,
    ProductReviewSerializer , CategoryValidateSerializer,
    ProductValidateSerializer , ReviewValidateSerializer

)


# Category
@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        return Response(data=CategoryListSerializer(categories, many=True).data)
    
    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        
        category = Category.objects.create(name=serializer.validated_data.get('name'))
        return Response(status=status.HTTP_201_CREATED, data=CategoryDetailSerializer(category).data)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(data=CategoryDetailSerializer(category).data)
    
    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        
        category.name = serializer.validated_data.get('name')
        category.save()
        return Response(status=status.HTTP_201_CREATED, data=CategoryDetailSerializer(category).data)
    
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Product
@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        return Response(data=ProductListSerializer(products, many=True).data)
    
    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        
        product = Product.objects.create(
            title=serializer.validated_data.get('title'),
            description=serializer.validated_data.get('description'),
            price=serializer.validated_data.get('price'),
            category_id=serializer.validated_data.get('category_id')
        )
        return Response(status=status.HTTP_201_CREATED, data=ProductDetailSerializer(product).data)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(data=ProductDetailSerializer(product).data)

    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        
        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category_id = serializer.validated_data.get('category_id')
        product.save()
        return Response(status=status.HTTP_201_CREATED, data=ProductDetailSerializer(product).data)
    
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def product_reviews_list_api_view(request):
    products = Product.objects.prefetch_related('reviews').all()
    data = ProductReviewSerializer(products, many=True).data
    return Response(data=data)


# Review
@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        return Response(data=ReviewListSerializer(reviews, many=True).data)
    
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        
        review = Review.objects.create(
            text=serializer.validated_data.get('text'),
            stars=serializer.validated_data.get('stars'),
            product_id=serializer.validated_data.get('product_id')
        )
        return Response(status=status.HTTP_201_CREATED, data=ReviewDetailSerializer(review).data)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(data=ReviewDetailSerializer(review).data)
    
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        
        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.product_id = serializer.validated_data.get('product_id')
        review.save()
        return Response(status=status.HTTP_201_CREATED, data=ReviewDetailSerializer(review).data)
    
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)