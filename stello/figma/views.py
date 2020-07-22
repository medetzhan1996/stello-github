import uuid
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from dal import autocomplete
from django.contrib.auth.models import User
from .models import Сategory, Product, ProductMaterial, Material
from .forms import CategoryForm, ProductForm


# List views
class IndexView(TemplateView):
    template_name = 'figma/client-site/index.html'

    def get(self, request, *args, **kwargs):
        author = get_object_or_404(User, id=self.kwargs['author'])
        kwargs.setdefault("author", author)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.kwargs['author']
        client_auth = self.request.session.get('client_auth')
        if not client_auth:
            client_auth = self.request.session['client_auth'] = str(
                uuid.uuid4())
        category = self.kwargs.get('category', None)
        context['categories'] = Сategory.objects.filter(
            author=author).all()
        context['client_auth'] = client_auth
        if not category:
            context['products'] = Product.objects.filter(
                is_top=True, author=author)[:12]
        else:
            context['category'] = get_object_or_404(Сategory, id=category)
            context['products'] = Product.objects.filter(
                category__id=category, author=author)[:12]
        return context


# Детальный просмотр продукта
class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'

    def get_template_names(self):
        if self.object.kind == 'text_input':
            return 'figma/client-site/product_text_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.kwargs['author']
        client_auth = self.request.session.get('client_auth')
        if not client_auth:
            client_auth = self.request.session['client_auth'] = str(
                uuid.uuid4())
        context['client_auth'] = client_auth
        context['product_materials'] = ProductMaterial.objects.filter(
            product__id=self.object.id).all()
        return context


# Главная страница менеджера
class ConstructorIndexView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'figma/constructor-site/index.html'
    category_form_class = CategoryForm
    product_form_class = ProductForm
    auth_categories = None
    products = None
    product = None
    category = None

    def dispatch(self, *args, **kwargs):
        self.categories = Сategory.objects.filter(
            author=self.request.user.id).all()
        self.products = Product.objects.filter(
            is_top=True, author=self.request.user.id)[:12]
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.GET.get('product_edit', None):
                self.product = get_object_or_404(
                    Product, id=request.GET.get('product_id'))
                return render(request, 'manager/product_modal.html',
                              {'product_form': self.product_form_class(
                                  request.user, instance=self.product),
                               'product': self.product})
            elif request.GET.get('category_edit', None):
                self.category = get_object_or_404(
                    Сategory, id=request.GET.get('category_id'))
                return render(request, 'manager/category_modal.html',
                              {'category_form': self.category_form_class(
                                  instance=self.category),
                               'category': self.category})
            elif request.GET.get('category_remove', None):
                self.category = get_object_or_404(
                    Сategory, id=request.GET.get('category_id'))
                return render(request, 'manager/category_remove_modal.html',
                              {'category': self.category})
            elif request.GET.get('product_remove', None):
                self.product = get_object_or_404(
                    Product, id=request.GET.get('product_id'))
                return render(request, 'manager/product_remove_modal.html',
                              {'product': self.product})
        return self.render_to_response(
            {
                'category_form': self.category_form_class(),
                'product_form': self.product_form_class(request.user),
                'categories': self.categories,
                'products': self.products,
                'product': self.product,
                'category': self.category
            })

    def post(self, request, *args, **kwargs):
        if request.POST.get('category-submit', None):
            category_id = request.POST.get('category_id', None)
            if category_id:
                category = get_object_or_404(Сategory, id=category_id)
                category_form = self.category_form_class(
                    request.POST, instance=category)
            else:
                category_form = self.category_form_class(request.POST)
            if category_form.is_valid():
                category_form.save()
        elif request.POST.get('product-submit', None):
            product_id = request.POST.get('product_id', None)
            if product_id:
                product = get_object_or_404(Product, id=product_id)
                product_form = self.product_form_class(
                    request.user, request.POST,
                    request.FILES, instance=product)
            else:
                product_form = self.product_form_class(
                    request.user, request.POST, request.FILES)
            if product_form.is_valid():
                product_form.save()
            else:
                print(product_form.errors)
        elif request.POST.get('category-remove-submit', None):
            Сategory.objects.filter(id=request.POST.get(
                'category_id'), author=request.user.id).delete()
        elif request.POST.get('product-remove-submit', None):
            Product.objects.filter(id=request.POST.get(
                'product_id'), author=request.user.id).delete()
        return redirect('manager:index')


# Mixin продукта
class ConstructorProductMixin(LoginRequiredMixin, TemplateResponseMixin, View):
    product_form_class = ProductForm
    product = None
    product_materials = None

    def dispatch(self, *args, **kwargs):
        self.proConstructorduct = get_object_or_404(
            Product, id=self.kwargs['id'])
        self.product_materials = ProductMaterial.objects.filter(
            product=self.kwargs['id']).all()
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        product_form = self.product_form_class(
            request.user, request.POST,
            request.FILES, instance=self.product)
        if product_form.is_valid():
            product_form.save()
            for material, price in zip(
                    request.POST.getlist('material_title'),
                    request.POST.getlist('material_price')):
                if material and price:
                    obj, created = Material.objects.get_or_create(
                        title=material)
                    q = ProductMaterial(material=obj, product=self.product,
                                        price=price)
                    q.save()
            if request.POST.get('send-material', None):
                return redirect('manager:product_detail', self.kwargs['id'])
            return redirect('manager:index')
        return self.render_to_response({
            'product': self.product, 'product_form': product_form,
            'product_materials': self.product_materials})


# Детальная информация текстового продукта
class ConstructorProductDetailView(ConstructorProductMixin):
    template_name = 'figma/constructor-site/product_text_detail.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            {
                'product': self.product,
                'product_form': self.product_form_class(
                    request.user, instance=self.product),
                'product_materials': self.product_materials
            })


# Детальная информация продукта c выбором изображения
class ConstructorProductPhotoDetailView(ConstructorProductMixin):
    template_name = 'figma/constructor-site/product_photo_detail.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            {
                'product': self.product,
                'product_form': self.product_form_class(
                    request.user, instance=self.product),
                'product_materials': self.product_materials
            })
