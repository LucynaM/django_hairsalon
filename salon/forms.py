from django import forms
from django.core.exceptions import ValidationError
from .models import MyUser, Service, Haircut, Holiday, Comment, Absence, NonOnlineCustomer
from .dates_handling import get_dates


class CustomerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = MyUser
        fields = ['username', 'password', 'password2', 'email', 'phone']

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
            'about': forms.Textarea(attrs={'cols': 80}),
        }


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'phone']


class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'about']
        widgets = {
            'about': forms.Textarea(attrs={'cols': 80}),
        }



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


HOURS = (
    (0, 'wszystkie'),
    (1, 'do 15 godz.'),
    (2, 'po 15 godz.'),
)

# haircut management

class SearchForm(forms.ModelForm):
    dates = forms.IntegerField(widget=forms.Select(choices=get_dates()))
    hours = forms.IntegerField(widget=forms.Select(choices=HOURS))
    staff = forms.ModelChoiceField(queryset=MyUser.objects.filter(is_staff=True), required=False)

    class Meta:
        model = Haircut
        fields = ['service', 'staff', 'dates', 'hours']


class ReservationForm(forms.ModelForm):
    class Meta:
        model = NonOnlineCustomer
        fields = '__all__'

class HaircutSearchForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    staff = forms.ModelChoiceField(queryset=MyUser.objects.filter(is_staff=True), required=False)


# service admin management
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(),
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
    start = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    end = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    staff = forms.ModelChoiceField(queryset=MyUser.objects.filter(is_staff=True))

