from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError


class CategoryListSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = 'id name products_count'.split()

    def get_products_count(self, category):
        return category.products.count() 


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars product'.split()


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title price category'.split()
        depth = 1


class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id title reviews rating'.split()

    def get_rating(self, product):
        reviews = product.reviews.all()
        if reviews.exists():
            return sum([i.stars for i in reviews]) / reviews.count()
        return 0


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=2, max_length=255)

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=2, max_length=255)
    description = serializers.CharField(required=False)
    price = serializers.IntegerField()
    category_id = serializers.IntegerField(min_value=1)

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Такой категории не существует!')
        return category_id
    


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product_id = serializers.IntegerField(min_value=1)

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('такого продукта не существует!')
        return product_id