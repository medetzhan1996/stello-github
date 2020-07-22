from django import forms
from .models import Сategory, Product, ProductMaterial


# Форма категории
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Сategory
        fields = ['title', 'author']


# Форма продукта
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, user, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Сategory.objects.filter(
            author=user.id)


# Форма материала продукта
class ProductMaterialForm(forms.ModelForm):
    class Meta:
        model = ProductMaterial
        fields = '__all__'
