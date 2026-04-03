from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category , Product , Review
from .serializers import CategoryListSerializer , CategoryDetailSerializer , ProductListSerializer , ProductReviewSerializer ,ProductDetailSerializer , ReviewListSerializer ,ReviewDetailSerializer


#Category

@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    data = CategoryDetailSerializer(category, many=False).data
    return Response(data=data)


@api_view(['GET'])
def category_list_api_view(request):
    category = Category.objects.all()
    list_ = CategoryListSerializer(category, many=True).data
    return Response(data=list_, 
                    status=status.HTTP_200_OK)


#Product

@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    data = ProductDetailSerializer(product, many=False).data
    return Response(data=data)


@api_view(['GET'])
def product_list_api_view(request):
    product = Product.objects.all()
    list_ = ProductListSerializer(product, many=True).data

    return Response(data=list_,
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def product_reviews_list_api_view(request):
    products = Product.objects.prefetch_related('reviews').all()
    list_ = ProductReviewSerializer(products, many=True).data
    return Response(data=list_, status=status.HTTP_200_OK)


#Review

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    data = ReviewDetailSerializer(review, many=False).data
    return Response(data=data)


@api_view(['GET'])
def review_list_api_view(request):
    review = Review.objects.all()
    list_ = ReviewListSerializer(review, many=True).data

    return Response(data=list_,
                    status=status.HTTP_200_OK)






