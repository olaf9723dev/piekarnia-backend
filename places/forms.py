from crispy_forms.bootstrap import InlineRadios
from crispy_forms.layout import Submit, ButtonHolder, Row, Column
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, Textarea, DateField, ChoiceField, RadioSelect, \
    DateInput, TextInput, TimeField, TimeInput

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from .models import Place, OpeningHours, CustomOpeningHours

DAY_OF_WEEK_CHOICES = (
    (1, 'Poniedziałek'),
    (2, 'Wtorek'),
    (3, 'Środa'),
    (4, 'Czwartek'),
    (5, 'Piątek'),
    (6, 'Sobota'),
    (7, 'Niedziela'),
)


def capitalized_validator(value):
    if value[0].islower():
        raise ValidationError('Wartość musi być pisana wielkimi literami.')


def number_validator(value):
    for v in value:
        if v in ['(', ')', '-'] or v.isdigit() or v.isspace():
            pass
        elif v.isalpha():
            raise ValidationError('W numerze telefonu nie może być litery.')
        else:
            raise ValidationError('W numerze telefonu nie może być innych znaków specjalnych, niż nawiasy lub myślnik.')


class PlaceForm(ModelForm):
    BOOLEAN_CHOICES = (
        (1, 'Włączony'),
        (0, 'Wyłączony'),
    )

    name = CharField(label='Nazwa Lokalu', max_length=1024, validators=[capitalized_validator],
                     widget=TextInput(attrs={'placeholder': 'Nazwa Lokalu'}))
    address = CharField(label='Adres', widget=TextInput(attrs={'placeholder': 'Adres'}))
    zip_code = CharField(label='Kod Pocztowy', widget=TextInput(attrs={'placeholder': 'Kod Pocztowy'}))
    city = CharField(label='Miasto', widget=TextInput(attrs={'placeholder': 'Miasto'}))
    description = CharField(label='Opis Lokalu', widget=Textarea(attrs={'placeholder': 'Opis Lokalu'}))
    is_enabled = ChoiceField(label='Status Lokalu', choices=BOOLEAN_CHOICES, widget=RadioSelect())
    enable_date = DateField(label='Data Włączenia Lokalu',
                            widget=DateInput(attrs={'type': 'date'}))
    telephone = CharField(label='Numer Telefonu', max_length=16, validators=[number_validator],
                          widget=TextInput(attrs={'placeholder': 'Numer Telefonu'}))

    class Meta:
        model = Place
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_read_only = True
        self.helper.form_id = 'id-place_form'
        self.helper.form_class = 'blueForms'
        self.helper.form_action = 'place_update'
        self.helper.form_method = 'post'
        self.helper.form_tag = True
        self.helper.disable_csrf = False
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('logo', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('address', css_class='form-group col-md-4 mb-0'),
                Column('zip_code', css_class='form-group col-md-4 mb-0'),
                Column('city', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('telephone', css_class='form-group col-md-4 mb-0'),
                InlineRadios('is_enabled', css_class='form-group col-md-4 mb-0'),  # InlineRadios
                Column('enable_date', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'description'
        )

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_description(self):
        initial = self.cleaned_data['description']
        result = []
        counter = 0
        for word in initial.split():
            if word.isspace():
                continue
            elif word in [',', '.']:
                result.append(word)
            elif counter == 0:
                result.append(word.capitalize())
                counter += 1
            else:
                result.append(" ")
                if result[-2] == '.':
                    result.append(word.capitalize())
                else:
                    result.append(word)

        return ''.join(el for el in result)


class PlaceCreateForm(PlaceForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.add_input(Submit('place_create', 'Dodaj Lokal', css_class='btn-primary'))
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('logo', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('address', css_class='form-group col-md-4 mb-0'),
                Column('zip_code', css_class='form-group col-md-4 mb-0'),
                Column('city', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('telephone', css_class='form-group col-md-4 mb-0'),
                Column('is_enabled', css_class='form-group col-md-4 mb-0'),
                Column('enable_date', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'description'
            # ButtonHolder(
            #     Submit('submit', 'Dodaj Lokal', css_class='btn-primary')
            # )
        )


class PlaceUpdateForm(PlaceForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-0'),
                Column('logo', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('address', css_class='form-group col-md-4 mb-0'),
                Column('zip_code', css_class='form-group col-md-4 mb-0'),
                Column('city', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('telephone', css_class='form-group col-md-4 mb-0'),
                Column('is_enabled', css_class='form-group col-md-4 mb-0'),
                Column('enable_date', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'description',
            ButtonHolder(
                Submit('submit', 'Aktualizuj Lokal', css_class='btn-primary')
            )
        )


class OpeningHoursForm(ModelForm):
    day_of_week = ChoiceField(label='Dzień Tygodnia', choices=DAY_OF_WEEK_CHOICES, required=False)
    start_time = TimeField(label='Godzina Otwarcia',
                           widget=TimeInput(attrs={'type': 'time', 'class': 'form_input', }, format='%H:%M'),
                           required=False)
    end_time = TimeField(label='Godzina Zamknięcia',
                         input_formats=['%H:%M'],
                         widget=TimeInput(attrs={'type': 'time', 'class': 'form_input', },
                                          format='%H:%M'),
                         required=False)

    class Meta:
        model = OpeningHours
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-opening_hours'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'opening_hours_create'
        self.helper.form_tag = True
        self.helper.field_class = 'col-lg-6'
        self.helper.disable_csrf = False
        self.helper.layout = Layout(
            Row(
                Column('day_of_week', css_class='form-group col-md-3 mb-0'),
                Column('start_time', css_class='form-group col-md-3 mb-0'),
                Column('end_time', css_class='form-group col-md-3 mb-0'),
                Column(
                    ButtonHolder(
                        Submit('submit', 'Dodaj / Aktualizuj Godziny Otwarcia', css_class='btn-primary')
                    ), css_class='form-group col-md-3 mb-0'
                ),
                css_class='form-row',
                style="asteriskField: none"
            )
        )


class CustomOpeningHoursForm(ModelForm):
    BOOLEAN_CHOICES = (
        (1, 'Zamknięty'),
        (0, 'Otwarty'),
    )

    date = DateField(label='Data', widget=DateInput(attrs={'type': 'date'}))
    start_time = TimeField(label='Godzina Otwarcia', widget=TimeInput(attrs={'type': 'time'}))
    end_time = TimeField(label='Godzina Zamknięcia', widget=TimeInput(attrs={'type': 'time'}))
    is_closed = ChoiceField(label='Status Lokalu', choices=BOOLEAN_CHOICES, widget=RadioSelect())

    class Meta:
        model = CustomOpeningHours
        fields = ('date', 'start_time', 'end_time', 'is_closed',)
