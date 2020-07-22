from django.db import models
from django.conf import settings
from tinymce.models import HTMLField


# Базовый абстрактный класс
class ItemBase(models.Model):
    title = models.CharField(max_length=180)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


# Список категории
class Сategory(ItemBase):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    class Meta:
        db_table = "figma_categories"


# материалы
class Material(ItemBase):
    pass

    class Meta:
        db_table = "figma_materials"


# Связь материала с продуктом М-М
class ProductMaterial(models.Model):
    material = models.ForeignKey(Material,
                                 related_name='rel_material',
                                 on_delete=models.CASCADE)
    product = models.ForeignKey('Product',
                                related_name='rel_product',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        db_table = "figma_products_materials"

    def __str__(self):
        return f'{self.material} rel {self.product}'


# список товаров
class Product(ItemBase):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    KIND_CHOICES = [
        ('normal', 'Обычный'),
        ('text_input', 'Набор текста'),
        ('image_select', 'Выбор изображения')
    ]
    category = models.ForeignKey(Сategory,
                                 related_name='products_category',
                                 on_delete=models.CASCADE)
    file = models.FileField(upload_to='images')
    file_extra1 = models.FileField(
        upload_to='images', blank=True, null=True)
    file_extra2 = models.FileField(
        upload_to='images', blank=True, null=True)
    file_extra3 = models.FileField(
        upload_to='images', blank=True, null=True)
    description = HTMLField(blank=True, null=True)
    details = HTMLField(blank=True, null=True)
    shipping_return = HTMLField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    price_old = models.DecimalField(max_digits=10, decimal_places=0,
                                    blank=True, null=True)
    is_top = models.BooleanField(default=False)
    kind = models.CharField(
        max_length=12,
        choices=KIND_CHOICES,
        default='normal'
    )
    classes = models.CharField(max_length=180, blank=True)
    materials = models.ManyToManyField(Material,
                                       through='ProductMaterial',
                                       related_name='rel_materials',
                                       blank=True, null=True)

    class Meta:
        db_table = "figma_products"
