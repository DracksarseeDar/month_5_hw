from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Укажите категорию')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(verbose_name='Укажите описание')
    price = models.PositiveIntegerField(verbose_name='Цена')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Продукт')
    author = models.CharField(max_length=100, verbose_name='Автор отзыва')
    text = models.TextField(max_length=322, verbose_name='Отзыв')
    rating = models.PositiveSmallIntegerField(default=5, verbose_name='Оценка')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Отзыв от {self.author} на {self.product.title}'