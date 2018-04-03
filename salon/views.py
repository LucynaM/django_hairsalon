from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import detail
from django.views.generic import list
from django.views.generic import edit
from django.http import Http404

from datetime import datetime

from .forms import HolidayForm, AbsenceForm, CustomerForm, StaffForm, CustomerUpdateForm, StaffUpdateForm, LoginForm, \
    SearchForm
from .models import MyUser, Service, Haircut, Absence, Holiday
from .dates_handling import get_absences, get_haircuts, get_user_calendar, return_date


def check_user(obj, request):
    if obj != request.user:
        raise Http404


class AdminUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class ServiceList(list.ListView):
    model = Service


class ServiceDetail(detail.DetailView):
    model = Service


class ServiceCreate(AdminUserPassesTestMixin, edit.CreateView):
    model = Service
    fields = '__all__'
    #
    # def test_func(self):
    #     return self.request.user.is_superuser


class ServiceUpdate(AdminUserPassesTestMixin, edit.UpdateView):
    model = Service
    fields = '__all__'


class ServiceDelete(AdminUserPassesTestMixin, edit.DeleteView):
    model = Service
    success_url = reverse_lazy('salon:service-list')
    
    
class AbsenceList(AdminUserPassesTestMixin, View):
    def get(self, request):
        absence_list = Absence.objects.filter(end__gte=datetime.now().date())
        ctx = {'absence_list': absence_list}
        return render(request, 'salon/absence_list.html', ctx)


class AbsenceDetail(AdminUserPassesTestMixin, detail.DetailView):
    model = Absence


class AbsenceCreate(AdminUserPassesTestMixin, View):

    def get(self, request):
        form = AbsenceForm()
        ctx = {'form': form}
        return render(request, 'salon/absence_form.html', ctx)

    def post(self, request):
        form = AbsenceForm(request.POST)
        if form.is_valid():
            absence = Absence.objects.create(**form.cleaned_data)
            print(absence)
            return redirect('salon:absence-detail', pk=absence.pk)

        ctx = {'form': form}
        return render(request, 'salon/absence_form.html', ctx)


class AbsenceUpdate(AdminUserPassesTestMixin, View):

    def get(self, request, pk):
        absence = Absence.objects.get(pk=pk)
        print(absence)
        form = AbsenceForm(initial={'start': absence.start,
                                    'end': absence.end,
                                    'staff': absence.staff})
        ctx = {'form': form}
        return render(request, 'salon/absence_update_form.html', ctx)

    def post(self, request, pk):
        form = AbsenceForm(request.POST)
        if form.is_valid():
            Absence.objects.filter(pk=pk).update(**form.cleaned_data)
            return redirect('salon:absence-detail', pk=pk)

        ctx = {'form': form}
        return render(request, 'salon/absence_form.html', ctx)


class AbsenceDelete(AdminUserPassesTestMixin, edit.DeleteView):
    model = Absence
    success_url = reverse_lazy('salon:absence-list')

    
class HolidayList(AdminUserPassesTestMixin, View):
    def get(self, request):
        holiday_list = Holiday.objects.filter(day__gte=datetime.now())
        ctx = {'holiday_list': holiday_list}
        return render(request, 'salon/holiday_list.html', ctx)


class HolidayDetail(AdminUserPassesTestMixin, detail.DetailView):
    model = Holiday


class HolidayCreate(AdminUserPassesTestMixin, edit.CreateView):
    form_class = HolidayForm
    model = Holiday


class HolidayUpdate(AdminUserPassesTestMixin, edit.UpdateView):
    model = Holiday
    fields = '__all__'


class HolidayDelete(AdminUserPassesTestMixin, edit.DeleteView):
    model = Holiday
    success_url = reverse_lazy('salon:holiday-list')


class CustomerCreate(View):
    """Sign up new customer"""

    def get(self, request):
        form = CustomerForm()
        ctx = {'form': form,}
        return render(request, 'salon/_customer_form_main.html', ctx)

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
        return render(request, 'salon/_customer_form_main.html', ctx)


class CustomerUpdate(View):
    """Update user"""

    def get(self, request, pk):
        customer = MyUser.objects.get(pk=pk)
        check_user(customer, request)
        form = CustomerUpdateForm(instance=customer)
        ctx = {'form': form,}
        return render(request, 'salon/customer_update_form.html', ctx)

    def post(self, request, pk):
        customer = MyUser.objects.get(pk=pk)
        form = CustomerUpdateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('salon:myuser-detail', pk=pk)
        ctx = {
            'form': form,
        }
        return render(request, 'salon/customer_update_form.html', ctx)


class StaffList(View):
    def get(self, request):
        staff_list = MyUser.objects.filter(is_staff=True)
        ctx = {'staff_list': staff_list}
        return render(request, 'salon/staff_list.html', ctx)


class StaffCreate(AdminUserPassesTestMixin, View):
    """Create staff"""

    def get(self, request):
        form = StaffForm()
        ctx = {'form': form,}
        return render(request, 'salon/staff_form.html', ctx)

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.cleaned_data.pop('password2')
            form.cleaned_data['is_staff'] = True
            user = MyUser.objects.create_user(**form.cleaned_data)
            return redirect('salon:myuser-detail', pk=user.pk)
        ctx = {
            'form': form,
        }
        return render(request, 'staff_form.html', ctx)



class StaffUpdate(AdminUserPassesTestMixin, View):
    """Update user"""

    def get(self, request, pk):
        staff = MyUser.objects.get(pk=pk)
        form = StaffUpdateForm(instance=staff)
        ctx = {'form': form,}
        return render(request, 'salon/staff_update_form.html', ctx)

    def post(self, request, pk):
        staff = MyUser.objects.get(pk=pk)
        form = StaffUpdateForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('salon:myuser-detail', pk=pk)
        ctx = {
            'form': form,
        }
        return render(request, 'salon/staff_update_form.html', ctx)


class UserDetail(detail.DetailView):
    model = MyUser


class UserDelete(edit.DeleteView):
    model = MyUser
    success_url = reverse_lazy('salon:myuser-list')


class LoginView(View):
    """Log in user"""

    def get(self, request):
        form = LoginForm()
        ctx = {
            'form': form
        }
        return render(request, 'salon/_login.html', ctx)

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
                    return redirect('salon:search')
            else:
                msg = "błędny użytkownik lub hasło"

        ctx = {
            'form': form,
            'msg': msg,
        }
        return render(request, 'salon/_login.html', ctx)


def logout_user(request):
    logout(request)
    return redirect('salon:login')


class SearchView(LoginRequiredMixin, View):

    def get(self, request):
        user = MyUser.objects.get(pk=request.user.id)
        haircuts = Haircut.objects.filter(customer=user).exclude(date__lte=datetime.now())
        form = SearchForm()
        ctx = {
            'haircuts': haircuts,
            'form': form,
        }
        return render(request, 'salon/_search.html', ctx)

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

            print(user_calendar)
            result = []
            for key, value in user_calendar.items():
                for date in value:
                    result.append((key, date))
            result = sorted(result, key=lambda date: date[1])
            print(result)


        ctx = {
            'form': form,
            'result': result,
            'service': service,
        }
        return render(request, 'salon/_search.html', ctx)


class ReservationView(LoginRequiredMixin, View):

    def get(self, request, date, user, service_id):
        reservation_date = return_date(date)
        staff = MyUser.objects.get(pk=user)
        service = Service.objects.get(pk=service_id)
        ctx = {
            'reservation_date': reservation_date,
            'staff': staff,
            'service': service,
        }

        return render(request, 'salon/reservation.html', ctx)

    def post(self, request, date, user, service_id):
        reservation_date = return_date(date)
        staff = MyUser.objects.get(pk=user)
        customer = MyUser.objects.get(pk=request.user.id)
        service = Service.objects.get(pk=service_id)
        haircut = Haircut.objects.create(date=reservation_date, staff=staff, customer=customer, service=service)
        ctx = {
            'haircut': haircut,
        }

        return render(request, 'salon/reservation.html', ctx)


class MainPage(View):
    # serve main page info
    def get(self, request):
        staff_list = MyUser.objects.filter(is_staff=True)
        service_list = Service.objects.all()
        ctx = {
            'staff_list': staff_list,
            'service_list': service_list,
        }
        return render(request, 'salon/_main-page.html', ctx)