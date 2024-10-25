from logging import getLogger

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import CategoryForm, CategoryUpdateForm, CategoryCreateForm, CategoryDeleteForm, VariantForm, \
    VariantCreateForm, VariantDeleteForm, VariantUpdateForm, VariantGroupForm, VariantGroupCreateForm, \
    VariantGroupDeleteForm, VariantGroupUpdateForm, ProductForm, ProductCreateForm, ProductDeleteForm, \
    ProductUpdateForm, ProductInPlaceCreateForm, ProductInPlaceUpdateForm, ProductInPlaceDeleteForm, ProductImageForm, \
    ProductImageDeleteForm, ProductImageUpdateForm, ProductImageCreateForm, ProductVariantForm
from .models import Category, Product, Variant, VariantGroup, ProductStatistic, ProductInPlace, ProductVariant, \
    ProductImage

LOGGER = getLogger()
class VariantGroupListView(ListView):
    template_name = 'categories/variant_group_list.html'
    model = VariantGroup
    query_set = VariantGroup.objects.all().order_by('name')
    context_object_name = 'variant_group'

class VariantGroupCreateView(CreateView):
    model = VariantGroup
    form_class = VariantGroupForm
    template_name = 'categories/variant_group_form.html'
    success_url = reverse_lazy('list_of_variant_group')
#     permission_required = 'variants.create_variant'

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        variant_group_form = VariantGroupCreateForm()
        message = 'Utwórz Nową Grupę Wariantów'
        context.update({
            "variant_group_form": variant_group_form,
            "message": message
        })
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
           LOGGER.warning(form)
           return super().form_invalid(form)



class VariantGroupUpdateView(UpdateView):
    model = VariantGroup
    form_class = VariantGroupForm
    template_name = 'categories/variant_group_form.html'
    success_url = reverse_lazy('list_of_variant_group')
    permission_required = 'variants.create_variant_group'

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        variant_group_form = VariantGroupUpdateForm(instance=context['object'])
        variant_group = VariantGroup.objects.get(pk=self.kwargs['pk'])
        message = f'Aktualizuj grupę atrybutów {variant.name}'
        context.update({
            "variant_form": variant_form,
            "message": message
        })
        return context

    def form_invalid(self, form):
        LOGGER.warning('Użytkownik podał nieprawidłowe dane podczas aktualizacji kategorii.')
        return super().form_invalid(form)


class VariantGroupDeleteView(DeleteView):
    model = VariantGroup
    template_name = 'categories/variant_group_form.html'
    success_url = reverse_lazy('list_of_variant_group')
    permission_required = 'variants.delete_variant'

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        variant_group_form = VariantGroupDeleteForm(instance=context['object'])
        context.update({
            "variant_group_form": variant_group_form
        })
        return context
#
class VariantsListView(ListView):
    template_name = 'categories/variants_list.html'
    model = Variant
    query_set = Variant.objects.all().order_by('name')
    context_object_name = 'variants'


class VariantCreateView(CreateView):
    model = Variant
    form_class = VariantForm
    template_name = 'categories/variant_form.html'
    success_url = reverse_lazy('list_of_variants')
#     permission_required = 'variants.create_variant'

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        variant_form = VariantCreateForm()
        message = 'Utwórz Nowy Atrybut'
        context.update({
            "variant_form": variant_form,
            "message": message
        })
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
           LOGGER.warning(form)
           return super().form_invalid(form)



class VariantUpdateView(UpdateView):
    model = Variant
    form_class = VariantForm
    template_name = 'categories/variant_form.html'
    success_url = reverse_lazy('list_of_variants')
    permission_required = 'variants.create_variant'

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        variant_form = VariantUpdateForm(instance=context['object'])
        variant = Variant.objects.get(pk=self.kwargs['pk'])
        message = f'Aktualizuj atrybut {variant.name}'
        context.update({
            "variant_form": variant_form,
            "message": message
        })
        return context

    def form_invalid(self, form):
        LOGGER.warning('Użytkownik podał nieprawidłowe dane podczas aktualizacji kategorii.')
        return super().form_invalid(form)


class VariantDeleteView(DeleteView):
    model = Variant
    template_name = 'categories/variant_form.html'
    success_url = reverse_lazy('list_of_variants')
    permission_required = 'variants.delete_variant'

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        variant_form = VariantDeleteForm(instance=context['object'])
        context.update({
            "variant_form": variant_form
        })
        return context
#
class CategoryListView(ListView):
    template_name = 'categories/categories_list.html'
    model = Category
    query_set = Category.objects.all().order_by('name')
    context_object_name = 'categories'


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('list_of_categories')
    permission_required = 'categories.create_category'

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category_form = CategoryCreateForm()
        message = 'Utwórz Nową Kategorię'
        context.update({
            "category_form": category_form,
            "message": message
        })
        return context

    def form_invalid(self, form):
        LOGGER.warning('Użytkownik podał nieprawidłowe dane.')
        return super().form_invalid(form)


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('list_of_categories')
    permission_required = 'categories.update_category'

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category_form = CategoryUpdateForm(instance=context['object'])
        category = Category.objects.get(pk=self.kwargs['pk'])
        message = f'Aktualizuj kategorię {category.name}'
        context.update({
            "category_form": category_form,
            "message": message
        })
        return context

    def form_invalid(self, form):
        LOGGER.warning('Użytkownik podał nieprawidłowe dane podczas aktualizacji kategorii.')
        return super().form_invalid(form)


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('list_of_categories')
    permission_required = 'categories.delete_category'

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category_form = CategoryDeleteForm(instance=context['object'])
        context.update({
            "category_form": category_form
        })
        return context

#
class ProductListView(ListView):
    template_name = 'categories/products_list.html'
    model = Product
    query_set = Product.objects.all().order_by('category__name')
    context_object_name = 'products'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'categories/product_form.html'
    success_url = reverse_lazy('list_of_products')
    permission_required = 'categories.create_product'

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product_form = ProductCreateForm()
        message = 'Utwórz Nowy Produkt'
        context.update({
            "product_form": product_form,
            "message": message
        })
        return context

    def form_invalid(self, form):
        LOGGER.warning('Użytkownik podał nieprawidłowe dane.')
        return super().form_invalid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'categories/product.html'
    success_url = reverse_lazy('list_of_products')
    permission_required = 'categories.update_products'

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product_form = ProductUpdateForm(instance=context['object'])
        product = Product.objects.get(pk=self.kwargs['pk'])
        variant_group = VariantGroup.objects.all().order_by('pk')
        variants = Variant.objects.all()
        images = ProductImage.objects.filter(product_id=self.kwargs['pk'])
        product_variant = ProductVariant.objects.filter(product = product)
        product_variant_variant = ProductVariant.objects.filter(product = product)
        product_variant_form = ProductVariantForm()

        try:
            statistics = ProductStatistic.objects.filter(product = product)
        except:
            statistics = {}

        message = f'Aktualizuj produkt {product.name}'
#         context = {
#         "product_form": product_form,
#         "message": message,
#         "statistics": statistics}
        context.update({
            "product_form": product_form,
            "message": message,
            "statistics": statistics,
            "variant_group": variant_group,
            "variants": variants,
            "images": images,
            "product_variant": product_variant,
            "product_variant_form": product_variant_form
        })
        return context

    def form_invalid(self, form):
        LOGGER.warning('Użytkownik podał nieprawidłowe dane podczas aktualizacji produktu.')
        return super().form_invalid(form)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'categories/product_form.html'
    success_url = reverse_lazy('list_of_products')
    permission_required = 'categories.delete_product'

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product_form = ProductDeleteForm(instance=context['object'])
        context.update({
            "product_form": product_form
        })
        return context


class ProductInPlaceCreateView(CreateView):
    model = ProductInPlace
    form_class = ProductInPlaceCreateForm
    template_name = 'categories/product_in_place_create.html'
    # permission_required = 'categories.create_product'

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product_in_place_form = ProductInPlaceCreateForm()
        product_in_place_form.fields['product'].queryset = Product.objects.exclude(id__in=[ProductInPlace.objects.filter(place_id=self.kwargs['place_id']).values_list('product_id')]).order_by('name')
        message = 'Utwórz Nowy Produkt'
        context.update({
            "product_in_place_form": product_in_place_form,
            "message": message,
            "place_id": self.kwargs['place_id']
        })
        return context

    def post(self, request, *args, **kwargs):
        place_id = self.kwargs['place_id']
        product, created = ProductInPlace.objects.get_or_create(
            place_id=place_id,
            product_id=int(request.POST.get('product'))
        )
        if created:
            product.custom_price = float(request.POST.get('custom_price'))
            for variant in request.POST.getlist('variant'):
                product.variant.add(ProductVariant.objects.get(pk=int(variant)))
            product.save()
        else:
            LOGGER.warning('Wybrany produkt już istnieje w tym lokalu')
            return render(request, 'categories/product_in_place_create.html', context={'place_id': place_id, 'product_in_place_form': ProductInPlaceCreateForm()})

        return redirect('place', place_id)

    def form_invalid(self, form):
        LOGGER.warning('Użytkownik podał nieprawidłowe dane.')
        return super().form_invalid(form)


class ProductInPlaceUpdateView(UpdateView):
    model = ProductInPlace
    form_class = ProductInPlaceUpdateForm
    template_name = 'categories/product_in_place.html'
    # permission_required = 'categories.update_products'

    def get_object(self, queryset=None):
        return ProductInPlace.objects.get(pk=self.kwargs['product_id'])

    def get_success_url(self):
        place_id = self.kwargs['place_id']
        return reverse_lazy('place', kwargs={"place_pk": place_id})

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product_in_place_form = ProductInPlaceUpdateForm(instance=context['object'])
        product = ProductInPlace.objects.get(pk=self.kwargs['product_id'])

        message = f'Aktualizuj produkt {product.product.name}'
        context.update({
            "product_in_place_form": product_in_place_form,
            "message": message,
            "place_id": self.kwargs['place_id'],
            "product_id": self.kwargs['product_id'],
            "product": product,
        })
        return context

    def form_invalid(self, form):
        LOGGER.warning('Użytkownik podał nieprawidłowe dane podczas aktualizacji produktu.')
        return super().form_invalid(form)


class ProductInPlaceDeleteView(DeleteView):
    model = ProductInPlace
    template_name = 'categories/product_in_place.html'
    # permission_required = 'categories.delete_product'

    def get_object(self, queryset=None):
        return ProductInPlace.objects.get(pk=self.kwargs['product_id'])

    def get_success_url(self):
        place_id = self.kwargs['place_id']
        return reverse_lazy('place', kwargs={"place_pk": place_id})

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product_in_place_form = ProductInPlaceDeleteForm(instance=context['object'])
        product = ProductInPlace.objects.get(pk=self.kwargs['product_id'])
        context.update({
            "product_in_place_form": product_in_place_form,
            "place_id": self.kwargs['place_id'],
            "product_id": self.kwargs['product_id'],
            "product": product,
        })
        return context


class ProductImageCreateView(CreateView):
    model = ProductImage
    form_class = ProductImageCreateForm
    template_name = 'categories/product_image_create.html'
    # permission_required = 'categories.create_product'

    # def get_success_url(self):
    #     product_id = self.kwargs['product_id']
    #     return reverse_lazy('product_update', kwargs={'pk': product_id})

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs['pk']
        image = ProductImage.objects.create(
            product_id=product_id,
            image=request.FILES.get('image'),
            is_primary=True if request.POST.get('is_primary') == 'true' else False,
            order=int(request.POST.get('order'))
        )

        return redirect('product_image_create', product_id)

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product_image_form = ProductImageCreateForm()
        message = 'Dodaj zdjęcie produktu'
        product = Product.objects.get(pk=self.kwargs['pk'])
        context.update({
            "product_image_form": product_image_form,
            "message": message,
            "product": product
        })
        return context

    def form_invalid(self, form):
        LOGGER.warning('Użytkownik podał nieprawidłowe dane.')
        return super().form_invalid(form)


class ProductImageUpdateView(UpdateView):
    model = ProductImage
    form_class = ProductImageUpdateForm
    template_name = 'categories/product_image_update.html'
    # permission_required = 'categories.update_products'

    def get_object(self, queryset=None):
        return ProductImage.objects.get(pk=self.kwargs['image_id'])

    # def get_success_url(self):
    #     product_id = self.kwargs['product_id']
    #     return reverse_lazy('product_update', kwargs={'pk': product_id})

    def post(self, request, *args, **kwargs):
        image_id = self.kwargs['image_id']
        product_id = self.kwargs['pk']
        image = ProductImage.objects.get(
            pk=image_id
        )
        image.delete()
        image = ProductImage.objects.create(
            product_id=product_id,
            image=request.FILES.get('image'),
            is_primary=True if request.POST.get('is_primary') == 'true' else False,
            order=int(request.POST.get('order'))
        )
        image.save()

        return redirect('product_update', product_id)

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product_image_form = ProductImageUpdateForm(instance=context['object'])
        product = Product.objects.get(pk=self.kwargs['pk'])
        context.update({
            "product_image_form": product_image_form,
            "product": product
        })
        return context

    def form_invalid(self, form):
        LOGGER.warning('Użytkownik podał nieprawidłowe dane podczas aktualizacji produktu.')
        return super().form_invalid(form)


class ProductImageDeleteView(DeleteView):
    model = ProductImage
    form_class = ProductImageDeleteForm
    template_name = 'categories/product_image_delete.html'
    # permission_required = 'categories.delete_product'

    def get_object(self, queryset=None):
        return ProductImage.objects.get(pk=self.kwargs['image_id'])

    # def get_success_url(self):
    #     product_id = self.kwargs['product_id']
    #     return reverse_lazy('product_update', kwargs={'pk': product_id})

    def post(self, request, *args, **kwargs):
        image_id = self.kwargs['image_id']
        product_id = self.kwargs['pk']
        image = ProductImage.objects.get(
            pk=image_id
        )
        image.delete()

        return redirect('product_update', product_id)

    def get_context_data(self, helper=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product_image_form = ProductImageDeleteForm(instance=context['object'])
        context.update({
            "product_image_form": product_image_form
        })
        return context


def create_product_variant(request, pk):
    if request.method == 'POST':
        if request.POST.get('prod_var_pk'):
            product_variant, created = ProductVariant.objects.get_or_create(pk=int(request.POST.get('prod_var_pk')))
        else:
            product_variant = ProductVariant.objects.create(
                product_id=pk
            )
            created = 1

        variant_groups = VariantGroup.objects.all()

        product_variant.extra_price = float(request.POST.get('extra_price', 0) or 0)
        product_variant.use_custom_stock = True if request.POST.get('use_custom_stock', 0) == 'on' else False
        product_variant.stock = float(request.POST.get('stock', 0) or 0)
        product_variant.unit = float(request.POST.get('unit', 0) or 0)
        product_variant.delivery_time = float(request.POST.get('delivery_time', 0) or 0)
        product_variant.weight = float(request.POST.get('weight', 0) or 0)
        product_variant.is_enabled = True if request.POST.get('is_enabled', 0) == 'on' else False

        if not created:
            try:
                product_variant.variant.through.objects.filter(productvariant_id=int(request.POST.get('prod_var_pk'))).delete()
            except:
                pass

        for variant in variant_groups:
            try:
                product_variant.variant.add(Variant.objects.get(pk=request.POST.get(f"select-{'-'.join((variant.name).split()).lower()}", '')))
            except:
                pass
        product_variant.save()

        return redirect('/catalog/list/{}/update_product'.format(product_variant.product.id))
