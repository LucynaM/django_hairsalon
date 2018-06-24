from django import forms
from django.core.exceptions import ValidationError
from .models import MyUser, Service, Holiday, NonOnlineCustomer
from .dates_handling import get_dates


class CustomerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Hasło')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Powtórzone hasło')

    class Meta:
        model = MyUser
        fields = ['username', 'password', 'password2', 'email', 'phone']
        help_texts = {
            'username': '',
        }

    def clean(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError('Hasła są różne')
        return self.cleaned_data


class StaffForm(CustomerForm):
    class Meta:
        model = MyUser
        fields = ['username', 'password', 'password2', 'first_name', 'last_name', 'email', 'phone', 'about']
        widgets = {
            'about': forms.Textarea(attrs={'rows':5, 'cols': 80}),
        }
        help_texts = {
            'username': '',
        }


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'phone']
        help_texts = {
            'username': '',
        }


class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'about']
        widgets = {
            'about': forms.Textarea(attrs={'rows':5, 'cols': 80}),
        }
        help_texts = {
            'username': '',
        }



class LoginForm(forms.Form):
    username = forms.CharField(label='Login')
    password = forms.CharField(widget=forms.PasswordInput(), label='Hasło')


HOURS = (
    (0, 'wszystkie'),
    (1, 'do 15 godz.'),
    (2, 'po 15 godz.'),
)

# haircut management

class SearchForm(forms.Form):
    service = forms.ModelChoiceField(queryset=Service.objects.all().order_by('name'))
    staff = forms.ModelChoiceField(queryset=MyUser.objects.filter(is_staff=True), required=False, label='Fryzjer')
    #dates = forms.IntegerField(widget=forms.Select(choices=get_dates()), label='Zakres dat')
    hours = forms.IntegerField(widget=forms.Select(choices=HOURS), label='Godziny')



class ReservationForm(forms.ModelForm):
    class Meta:
        model = NonOnlineCustomer
        fields = '__all__'

class HaircutSearchForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='Data')
    staff = forms.ModelChoiceField(queryset=MyUser.objects.filter(is_staff=True), required=False, label='Fryzjer')


# service admin management
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows':4, 'cols': 80}),
        }


# holiday admin management
class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = '__all__'
        widgets = {
            'day': forms.DateInput(attrs={'type': 'date'}),
        }


# absence admin management
class AbsenceForm(forms.Form):
    start = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='Początek')
    end = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label='Koniec')
    staff = forms.ModelChoiceField(queryset=MyUser.objects.filter(is_staff=True), label='Pracownik')

