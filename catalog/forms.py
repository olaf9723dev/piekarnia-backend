from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, ButtonHolder, Submit
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, TextInput, ChoiceField

from .models import Category, Variant, VariantGroup, Product, ProductInPlace, ProductImage, ProductVariant


def capitalized_validator(value):
    if value[0].islower():
        raise ValidationError('Wartość musi być pisana wielkimi literami.')


#
class VariantGroupForm(ModelForm):
    name = CharField(label='Nazwa Atrybutu', max_length=128,
                     widget=TextInput(attrs={'placeholder': 'Nazwa Atrybutu'}))

    class Meta:
        model = VariantGroup
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_read_only = True
        self.helper.form_id = 'id-variantGroup_form'
        self.helper.form_action = 'variantGroup'
        self.helper.form_tag = False
        self.helper.disable_csrf = False
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('group_type', css_class='form-group col-md-4 mb-0'),
                Column('max_selected_count', css_class='form-group col-md-2 mb-0'),
                Column('min_selected_count', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            )
        )

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class VariantGroupCreateForm(VariantGroupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('group_type', css_class='form-group col-md-4 mb-0'),
                Column('max_selected_count', css_class='form-group col-md-2 mb-0'),
                Column('min_selected_count', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Dodaj nową grupę wariantów', css_class='btn-primary')
            )
        )


class VariantGroupUpdateForm(VariantGroupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('group_type', css_class='form-group col-md-4 mb-0'),
                Column('max_selected_count', css_class='form-group col-md-2 mb-0'),
                Column('min_selected_count', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Aktualizuj Kategorię', css_class='btn-primary')
            )
        )


class VariantGroupDeleteForm(VariantGroupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('group_type', css_class='form-group col-md-4 mb-0'),
                Column('max_selected_count', css_class='form-group col-md-2 mb-0'),
                Column('min_selected_count', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Usuń Grupę wariantów', css_class='btn-danger')
            )
        )


#
class VariantForm(ModelForm):
    name = CharField(label='Nazwa Atrybutu', max_length=128,
                     widget=TextInput(attrs={'placeholder': 'Nazwa Atrybutu'}))

    class Meta:
        model = Variant
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_read_only = True
        self.helper.form_id = 'id-variant_form'
        self.helper.form_action = 'variant'
        self.helper.form_tag = False
        self.helper.disable_csrf = False
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('group', css_class='form-group col-md-4 mb-0'),
                Column('extra_price', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            )
        )

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class VariantCreateForm(VariantForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('group', css_class='form-group col-md-4 mb-0'),
                Column('extra_price', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Dodaj Atrybut', css_class='btn-primary')
            )
        )


class VariantUpdateForm(VariantForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('group', css_class='form-group col-md-4 mb-0'),
                Column('extra_price', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Aktualizuj Kategorię', css_class='btn-primary')
            )
        )


class VariantDeleteForm(VariantForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('group', css_class='form-group col-md-4 mb-0'),
                Column('extra_price', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Usuń Kategorię', css_class='btn-danger')
            )
        )


#
class CategoryForm(ModelForm):
    BOOLEAN_CHOICES = (
        (1, 'Włączona'),
        (0, 'Wyłączona'),
    )

    name = CharField(label='Nazwa Kategorii', max_length=128, validators=[capitalized_validator],
                     widget=TextInput(attrs={'placeholder': 'Nazwa Kategorii'}))
    is_enabled = ChoiceField(label='Status Kategorii', choices=BOOLEAN_CHOICES)

    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_read_only = True
        self.helper.form_id = 'id-category_form'
        self.helper.form_class = 'category'
        self.helper.form_action = 'category'
        self.helper.form_tag = False
        self.helper.disable_csrf = False
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('image', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('is_enabled', css_class='form-group col-md-6 mb-0'),
                Column('parent', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CategoryCreateForm(CategoryForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('image', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('is_enabled', css_class='form-group col-md-6 mb-0'),
                Column('parent', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Dodaj Kategorię', css_class='btn-primary')
            )
        )


class CategoryUpdateForm(CategoryForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('image', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('is_enabled', css_class='form-group col-md-6 mb-0'),
                Column('parent', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Aktualizuj Kategorię', css_class='btn-primary')
            )
        )


class CategoryDeleteForm(CategoryForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('image', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('is_enabled', css_class='form-group col-md-6 mb-0'),
                Column('parent', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Usuń Kategorię', css_class='btn-danger')
            )
        )


#
class ProductForm(ModelForm):
    name = CharField(label='Nazwa Produktu', max_length=128,
                     widget=TextInput(attrs={'placeholder': 'Nazwa Atrybutu'}))

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_read_only = True
        self.helper.form_id = 'id-product_form'
        self.helper.form_action = 'product'
        self.helper.form_tag = False
        self.helper.disable_csrf = False
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('category', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('net_price', css_class='form-group col-md-3 mb-0'),
                Column('vat_base', css_class='form-group col-md-3 mb-0'),
                Column('is_promo', css_class='form-group col-md-3 mb-0'),
                Column('is_new', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('short_description', css_class='form-group col-md-6 mb-0'),
                Column('description', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('similar_products', css_class='form-group col-md-6 mb-0'),
                Column('tags', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('is_enabled', css_class='form-group col-md-1 mb-0'),
                Column('product_code', css_class='form-group col-md-3 mb-0'),
            ),
        )

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProductCreateForm(ProductForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('category', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('net_price', css_class='form-group col-md-3 mb-0'),
                Column('vat_base', css_class='form-group col-md-3 mb-0'),
                Column('is_promo', css_class='form-group col-md-3 mb-0'),
                Column('is_new', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('short_description', css_class='form-group col-md-6 mb-0'),
                Column('description', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('similar_products', css_class='form-group col-md-6 mb-0'),
                Column('tags', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('is_enabled', css_class='form-group col-md-1 mb-0'),
                Column('product_code', css_class='form-group col-md-3 mb-0'),
            ),
            ButtonHolder(
                Submit('submit', 'Dodaj Atrybut', css_class='btn-primary')
            )
        )


class ProductUpdateForm(ProductForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('category', css_class='form-group col-md-4 mb-0'),
                Column('net_price', css_class='form-group col-md-2 mb-0'),
                Column('vat_base', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('short_description', css_class='form-group col-md-6 mb-0'),
                Column('description', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('similar_products', css_class='form-group col-md-6 mb-0'),
                Column('tags', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('is_enabled', css_class='form-group col-md-2 mb-0'),
                Column('is_promo', css_class='form-group col-md-2 mb-0'),
                Column('is_new', css_class='form-group col-md-2 mb-0'),
                Column('product_code', css_class='form-group col-md-3 mb-0'),
            ),
            ButtonHolder(
                Submit('submit', 'Aktualizuj produkt', css_class='btn-primary')
            )
        )


class ProductDeleteForm(ProductForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('category', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('net_price', css_class='form-group col-md-3 mb-0'),
                Column('vat_base', css_class='form-group col-md-3 mb-0'),
                Column('is_promo', css_class='form-group col-md-3 mb-0'),
                Column('is_new', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('short_description', css_class='form-group col-md-6 mb-0'),
                Column('description', css_class='form-group col-md-6 mb-0'),
            ),
            Row(
                Column('similar_products', css_class='form-group col-md-6 mb-0'),
                Column('tags', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('is_enabled', css_class='form-group col-md-1 mb-0'),
                Column('product_code', css_class='form-group col-md-3 mb-0'),
            ),
            ButtonHolder(
                Submit('submit', 'Usuń produkt', css_class='btn-danger')
            )
        )


class ProductInPlaceForm(ModelForm):

    class Meta:
        model = ProductInPlace
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_read_only = True
        self.helper.form_id = 'id-product_in_place_form'
        self.helper.form_action = 'product'
        self.helper.form_tag = False
        self.helper.disable_csrf = False
        self.helper.layout = Layout(
            Row(
                Column('product', css_class='form-group col-md-6 mb-0'),
                Column('variant', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('place', css_class='form-group col-md-6 mb-0'),
                Column('custom_price', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProductInPlaceCreateForm(ProductInPlaceForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('product', css_class='form-group col-md-8 mb-0'),
                Column('custom_price', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('variant', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Utwórz nowy produkt', css_class='btn-primary')
            )
        )


class ProductInPlaceUpdateForm(ProductInPlaceForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('product', css_class='form-group col-md-6 mb-0'),
                Column('variant', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('place', css_class='form-group col-md-6 mb-0'),
                Column('custom_price', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Aktualizuj produkt', css_class='btn-primary')
            )
        )


class ProductInPlaceDeleteForm(ProductInPlaceForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('product', css_class='form-group col-md-6 mb-0'),
                Column('variant', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('place', css_class='form-group col-md-6 mb-0'),
                Column('custom_price', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Usuń produkt', css_class='btn-primary')
            )
        )


class ProductImageForm(ModelForm):

    class Meta:
        model = ProductImage
        exclude = ['product']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_read_only = True
        self.helper.form_id = 'id-product_image_form'
        self.helper.form_action = 'product'
        self.helper.form_tag = False
        self.helper.disable_csrf = False
        self.helper.layout = Layout(
            Row(
                # Column('product', css_class='form-group col-md-6 mb-0'),
                Column('image', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('is_primary', css_class='form-group col-md-6 mb-0'),
                Column('order', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProductImageCreateForm(ProductImageForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                # Column('product', css_class='form-group col-md-6 mb-0'),
                Column('image', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('is_primary', css_class='form-group col-md-6 mb-0'),
                Column('order', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Dodaj zdjęcie', css_class='btn-primary')
            )
        )


class ProductImageUpdateForm(ProductImageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('product', css_class='form-group col-md-6 mb-0'),
                Column('image', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('is_primary', css_class='form-group col-md-6 mb-0'),
                Column('order', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Aktualizuj zdjęcie', css_class='btn-primary')
            )
        )


class ProductImageDeleteForm(ProductImageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('product', css_class='form-group col-md-6 mb-0'),
                Column('image', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('is_primary', css_class='form-group col-md-6 mb-0'),
                Column('order', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                Submit('submit', 'Usuń zdjęcie', css_class='btn-primary')
            )
        )


class ProductVariantForm(ModelForm):
    class Meta:
        model = ProductVariant
        exclude = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_read_only = True
        self.helper.form_id = 'id-product_image_form'
        self.helper.form_action = 'product'
        self.helper.form_tag = False
        self.helper.disable_csrf = False
        self.helper.layout = Layout(
             Row(
                 Column('is_enabled', css_class='form-group col-md-4 mb-0'),
                 Column('use_custom_stock', css_class='form-group col-md-4 mb-0'),
                 Column('delivery_time', css_class='form-group col-md-4 mb-0'),
                 css_class='form-row'
             ),
             Row(
                 Column('product', css_class='form-group col-md-8 mb-0'),
                 Column('extra_price', css_class='form-group col-md-4 mb-0'),
                 css_class='form-row'
             ),
             Row(
                 Column('variant', css_class='form-group col-md-8 mb-0'),
                 Column('extra_price', css_class='form-group col-md-4 mb-0'),
                 css_class='form-row'
             ),
             Row(
                 Column('stock', css_class='form-group col-md-4 mb-0'),
                 Column('unit', css_class='form-group col-md-4 mb-0'),
                 Column('weight', css_class='form-group col-md-4 mb-0'),
                 css_class='form-row'
             ),
        )

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProductVariantCreateForm(ProductImageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
             Row(
                 Column('is_enabled', css_class='form-group col-md-4 mb-0'),
                 Column('use_custom_stock', css_class='form-group col-md-4 mb-0'),
                 Column('delivery_time', css_class='form-group col-md-4 mb-0'),
                 css_class='form-row'
             ),
             Row(
                 Column('product', css_class='form-group col-md-8 mb-0'),
                 Column('extra_price', css_class='form-group col-md-4 mb-0'),
                 css_class='form-row'
             ),
             Row(
                 Column('variant', css_class='form-group col-md-8 mb-0'),
                 Column('extra_price', css_class='form-group col-md-4 mb-0'),
                 css_class='form-row'
             ),
             Row(
                 Column('stock', css_class='form-group col-md-4 mb-0'),
                 Column('unit', css_class='form-group col-md-4 mb-0'),
                 Column('weight', css_class='form-group col-md-4 mb-0'),
                 css_class='form-row'
             ),
            ButtonHolder(
                Submit('submit', 'Dodaj produkt', css_class='btn-primary')
            )
        )
