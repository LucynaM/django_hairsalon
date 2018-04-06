from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from django.http import Http404

from datetime import datetime

from .forms import HolidayForm, AbsenceForm, CustomerForm, StaffForm, CustomerUpdateForm, StaffUpdateForm, LoginForm, \
    SearchForm, ServiceForm, HolidayForm, ReservationForm, HaircutSearchForm
from .models import MyUser, Service, Haircut, Absence, Holiday, NonOnlineCustomer
from .dates_handling import get_absences, get_absence_days, get_haircuts, get_user_calendar, return_date


def check_user(obj, request):
    if obj != request.user:
        raise Http404


class AdminUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class MainPage(View):
    # serve main page info
    def get(self, request):
        staff_list = MyUser.objects.filter(is_staff=True)
        service_list = Service.objects.all()
        ctx = {
            'staff_list': staff_list,
            'service_list': service_list,
        }
        return render(request, 'salon/main.html', ctx)


class LoginView(View):
    """Log in user"""

    def get(self, request):
        form = LoginForm()
        ctx = {
            'form': form
        }
        return render(request, 'salon/login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        msg = ""
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    # if user.is_superuser redirect to salon:admin
                    return redirect('salon:search')
            else:
                msg = "błędny użytkownik lub hasło"

        ctx = {
            'form': form,
            'msg': msg,
        }
        return render(request, 'salon/login.html', ctx)


def logout_user(request):
    logout(request)
    return redirect('salon:main')


class SearchView(LoginRequiredMixin, View):

    def get(self, request):
        user = MyUser.objects.get(pk=request.user.id)
        haircuts = Haircut.objects.filter(customer=user).exclude(date__lte=datetime.now())
        form = SearchForm()
        ctx = {
            'haircuts': haircuts,
            'form': form,
        }
        return render(request, 'salon/search.html', ctx)

    def post(self, request):
        form = SearchForm(request.POST)
        user_calendar = None
        service = None
        if form.is_valid():

            # pobieramy 0, 1, 2, 3 - reprezentację tygodni, która posłuży do ustawienia dat
            day_choice = form.cleaned_data['dates']

            # pobieramy wolne dni
            holidays = [holiday.day for holiday in Holiday.objects.all()]
            # pobieramy zakres godzin i przekuwamy go na dane potrzebne w forze
            hours = form.cleaned_data['hours']
            start_hour = 0
            end_hour = 8
            if hours == 1:
                start_hour = 0
                end_hour = 4
            elif hours == 2:
                start_hour = 4
                end_hour = 8
            # pobieramy fryzjera
            staff = form.cleaned_data['staff']
            # jeżeli nie wybrano żadnego, pobieramy wszystkich lub zgodnie z wyborem, nastęþnie wrzucamy ich do tablicy
            staff_selection = []
            if not staff:
                staff_selection = [user for user in MyUser.objects.filter(is_staff=True)]
            else:
                staff_selection.append(staff)

            # uruchamiamy funkcję zwracającą słownik z nieobecnościami per fryzjer
            absences = get_absences(staff_selection)

            # uruchamiamy funkcję zwracającą słownik z godzinami zajętymi per fryzjer
            haircuts = get_haircuts(staff_selection)

            # czas trwania usługi
            service = form.cleaned_data['service']
            service_duration = int(service.duration / 60)

            # uruchamiamy funkcję generującą kalendarz
            user_calendar = {}
            for user in staff_selection:
                user_calendar[user] = get_user_calendar(day_choice,
                                                        holidays,
                                                        user,
                                                        absences,
                                                        haircuts,
                                                        start_hour,
                                                        end_hour,
                                                        service_duration)

            # split user_calendar into tuples (user, date) in order to order it by dates
            result = []
            for key, value in user_calendar.items():
                for date in value:
                    result.append((key, date))
            result = sorted(result, key=lambda date: date[1])

        ctx = {
            'form': form,
            'result': result,
            'service': service,
        }
        return render(request, 'salon/search.html', ctx)


class ReservationView(LoginRequiredMixin, View):

    def get(self, request, date, user, service_id):
        form = ReservationForm()
        reservation_date = return_date(date)
        staff = MyUser.objects.get(pk=user)
        service = Service.objects.get(pk=service_id)
        ctx = {
            'form': form,
            'reservation_date': reservation_date,
            'staff': staff,
            'service': service,
        }

        return render(request, 'salon/reservation.html', ctx)

    def post(self, request, date, user, service_id):

        new_haircut = {}
        new_haircut['date'] = return_date(date)
        new_haircut['staff'] = MyUser.objects.get(pk=user)
        new_haircut['customer'] = MyUser.objects.get(pk=request.user.id)
        new_haircut['service'] = Service.objects.get(pk=service_id)
        form = ReservationForm(request.POST)
        if form.is_valid():
            non_online_customer_list = NonOnlineCustomer.objects.filter(**form.cleaned_data)
            if non_online_customer_list:
                non_online_customer = non_online_customer_list[0]
            else:
                non_online_customer = form.save()
            new_haircut['non_online_customer'] = non_online_customer

        Haircut.objects.create(**new_haircut)

        return redirect('salon:search')


class CustomerDelete(View):

    def get(self, request, pk):
        user = MyUser.objects.get(pk=pk)
        check_user(user, request)
        ctx = {
            'user': user,
        }
        return render(request, 'salon/customer_delete.html', ctx)

    def post(self, request, pk):
        user = MyUser.objects.get(pk=pk)
        user.delete()
        return redirect('salon:main')


class CustomerCreate(View):
    """Sign up new customer"""

    def get(self, request):
        form = CustomerForm()
        ctx = {'form': form,}
        return render(request, 'salon/customer_add.html', ctx)

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.cleaned_data.pop('password2')
            user = MyUser.objects.create_user(**form.cleaned_data)
            login(request, user)
            return redirect('salon:search')
        ctx = {
            'form': form,
        }
        return render(request, 'salon/customer_add.html', ctx)


class CustomerUpdate(View):
    """Update user"""

    def get(self, request, pk):
        customer = MyUser.objects.get(pk=pk)
        check_user(customer, request)
        form = CustomerUpdateForm(instance=customer)
        ctx = {'form': form,}
        return render(request, 'salon/customer_edit.html', ctx)

    def post(self, request, pk):
        customer = MyUser.objects.get(pk=pk)
        form = CustomerUpdateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('salon:search')
        ctx = {
            'form': form,
        }
        return render(request, 'salon/customer_edit.html', ctx)


# services admin management


class SeviceListAdd(AdminUserPassesTestMixin, View):
    def get(self, request):
        service_list = Service.objects.all()
        form = ServiceForm()
        ctx = {
            'service_list': service_list,
            'form': form,
               }
        return render(request, 'salon/service.html', ctx)

    def post(self, request):
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = Service.objects.create(**form.cleaned_data)
        service_list = Service.objects.all()
        ctx = {
            'service_list': service_list,
            'form': form,
        }
        return render(request, 'salon/service.html', ctx)


class ServiceEditDelete(AdminUserPassesTestMixin, View):
    def get(self, request, pk):
        service = Service.objects.get(pk=pk)
        form = ServiceForm(instance=service)
        ctx = {
            'form': form,
        }
        return render(request, 'salon/service_edit.html', ctx)

    def post(self, request, pk):
        service = Service.objects.get(pk=pk)
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            if request.POST['submit'] == 'edit':
                form.save()
            elif request.POST['submit'] == 'delete':
                service.delete()
            return redirect('salon:service')
        ctx = {
            'form': form,
        }
        return render(request, 'salon/service_edit.html', ctx)



# staff admin management

class StaffListAdd(AdminUserPassesTestMixin, View):
    """Create, list staff"""

    def get(self, request):
        staff_list = MyUser.objects.filter(is_staff=True)
        form = StaffForm()
        ctx = {
            'form': form,
            'staff_list': staff_list,
        }
        return render(request, 'salon/staff.html', ctx)

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.cleaned_data.pop('password2')
            form.cleaned_data['is_staff'] = True
            MyUser.objects.create_user(**form.cleaned_data)
        staff_list = MyUser.objects.filter(is_staff=True)
        ctx = {
            'form': form,
            'staff_list': staff_list,
        }
        return render(request, 'salon/staff.html', ctx)



class StaffEditDelete(AdminUserPassesTestMixin, View):
    """Update user"""

    def get(self, request, pk):
        staff = MyUser.objects.get(pk=pk)
        form = StaffUpdateForm(instance=staff)
        ctx = {
            'form': form,
        }
        return render(request, 'salon/staff_edit.html', ctx)

    def post(self, request, pk):
        staff = MyUser.objects.get(pk=pk)
        form = StaffUpdateForm(request.POST, instance=staff)
        if form.is_valid():
            if request.POST['submit'] == 'edit':
                form.save()
            elif request.POST['submit'] == 'delete':
                staff.delete()
            return redirect('salon:staff')
        ctx = {
            'form': form,
        }
        return render(request, 'salon/staff_edit.html', ctx)


# absences admin management
class AbsenceListAdd(AdminUserPassesTestMixin, View):

    def get(self, request):
        absence_list = Absence.objects.filter(end__gte=datetime.now().date())
        form = AbsenceForm()
        ctx = {
            'form': form,
            'absence_list': absence_list,
           }
        return render(request, 'salon/absence.html', ctx)

    def post(self, request):
        form = AbsenceForm(request.POST)
        if form.is_valid():
            absence = Absence.objects.create(**form.cleaned_data)
        # check list of staff haircuts when new absence is added
        haircuts = Haircut.objects.filter(staff=absence.staff).exclude(date__lte=datetime.now())
        haircut_list = []
        for haircut in haircuts:
            if haircut.date.date() in get_absence_days(absence):
                haircut_list.append(haircut)
        absence_list = Absence.objects.filter(end__gte=datetime.now().date())

        ctx = {
            'form': form,
            'absence_list': absence_list,
            'haircuts_list': haircut_list,
        }
        return render(request, 'salon/absence.html', ctx)


class AbsenceEditDelete(AdminUserPassesTestMixin, View):

    def get(self, request, pk):
        absence = Absence.objects.get(pk=pk)
        form = AbsenceForm(initial={'start': absence.start,
                                    'end': absence.end,
                                    'staff': absence.staff})
        ctx = {'form': form}
        return render(request, 'salon/absence_edit.html', ctx)

    def post(self, request, pk):
        form = AbsenceForm(request.POST)
        if form.is_valid():
            if request.POST['submit'] == 'edit':
                Absence.objects.filter(pk=pk).update(**form.cleaned_data)
            elif request.POST['submit'] == 'delete':
                absence = Absence.objects.get(pk=pk)
                absence.delete()
            return redirect('salon:absence')

        ctx = {'form': form}
        return render(request, 'salon/absence_edit.html', ctx)


# holidays admin management

class HolidayListAdd(AdminUserPassesTestMixin, View):

    def get(self, request):
        holiday_list = Holiday.objects.filter(day__gte=datetime.now())
        form = HolidayForm()
        ctx = {
            'holiday_list': holiday_list,
            'form': form,
               }
        return render(request, 'salon/holiday.html', ctx)

    def post(self, request):
        form = HolidayForm(request.POST)
        if form.is_valid():
            Holiday.objects.create(**form.cleaned_data)
        holiday_list = Holiday.objects.filter(day__gte=datetime.now())
        ctx = {
            'holiday_list': holiday_list,
            'form': form,
        }
        return render(request, 'salon/holiday.html', ctx)


class HolidayEditDelete(AdminUserPassesTestMixin, View):

    def get(self, request, pk):
        holiday = Holiday.objects.get(pk=pk)
        form = HolidayForm(instance=holiday)
        ctx = {
            'form': form,
        }
        return render(request, 'salon/holiday_edit.html', ctx)

    def post(self, request, pk):
        holiday = Holiday.objects.get(pk=pk)
        form = HolidayForm(request.POST, instance=holiday)
        if form.is_valid():
            if request.POST['submit'] == 'edit':
                form.save()
            elif request.POST['submit'] == 'delete':
                holiday.delete()
            return redirect('salon:holiday')
        ctx = {
            'form': form,
        }
        return render(request, 'salon/holiday_edit.html', ctx)

# haircuts admin management


class HaircutDelete(View):

    def get(self, request, pk):
        haircut = Haircut.objects.get(pk=pk)
        check_user(haircut.customer, request)
        ctx = {
            'haircut': haircut,
        }
        return render(request, 'salon/haircut_delete.html', ctx)

    def post(self, request, pk):
        haircut = Haircut.objects.get(pk=pk)
        haircut.delete()
        return redirect('salon:search')


class HaircutList(View):

    def get_day_haircuts(self, start, end, **kwargs):
        haircut_list = []
        for haircut in Haircut.objects.filter(date__range=(start, end), **kwargs):
            haircut_list.append(haircut)
        return haircut_list

    def get(self, request):
        start = datetime.now().replace(hour=11, minute=00, second=00, microsecond=000000)
        end = datetime.now().replace(hour=19, minute=00, second=00, microsecond=000000)
        haircut_list = self.get_day_haircuts(start, end)
        form = HaircutSearchForm()
        ctx = {
            'haircut_list': haircut_list,
            'form': form,
        }
        return render(request, 'salon/haircut.html', ctx)

    def post(self, request):
        form = HaircutSearchForm(request.POST)
        haircut_list = None
        if form.is_valid():
            date = form.cleaned_data['date']
            start = datetime(year=date.year, month=date.month, day=date.day, hour=11, minute=00, second=00, microsecond=000000)
            end = datetime(year=date.year, month=date.month, day=date.day, hour=19, minute=00, second=00, microsecond=000000)
            haircut_staff = {}
            if form.cleaned_data['staff']:
                haircut_staff = {'staff': form.cleaned_data['staff']}
            haircut_list = self.get_day_haircuts(start, end, **haircut_staff)
        ctx = {
            'haircut_list': haircut_list,
            'form': form,
        }
        return render(request, 'salon/haircut.html', ctx)

