from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название категории")

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название товара")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    price = models.IntegerField(verbose_name="Цена")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products', 
        null=True, 
        verbose_name="Категория"
    )

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    stars = models.IntegerField(
        choices=((i, i) for i in range(1, 6)), 
        default=5, 
        verbose_name="Рейтинг (1-5)"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='reviews', 
        verbose_name="Товар"
    )

    def __str__(self):
        return f"Отзыв на {self.product.title}"