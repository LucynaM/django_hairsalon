from django.conf.urls import url
from .views import CustomerCreate, CustomerUpdate, CustomerDelete, \
    MainPage, LoginView, logout_user, SearchView, ReservationView, \
    HaircutDelete, HaircutList, \
    SeviceListAdd, ServiceEditDelete, StaffListAdd, StaffEditDelete, \
    AbsenceListAdd, AbsenceEditDelete, HolidayListAdd, HolidayEditDelete

urlpatterns = [
    url(r'^main/$', MainPage.as_view(), name='main'),

    url(r'^customer/delete/(?P<pk>[0-9]+)/$', CustomerDelete.as_view(), name='customer-delete'),
    url(r'^customer/add/$', CustomerCreate.as_view(), name='customer-add'),
    url(r'^customer/edit/(?P<pk>[0-9]+)/$', CustomerUpdate.as_view(), name='customer-edit'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^reserve/(?P<date>([a-zA-Z0-9\-:])+)/(?P<user>(\d)+)/(?P<service_id>(\d)+)/$', ReservationView.as_view(),
        name='reservation'),

    url(r'^service/$', SeviceListAdd.as_view(), name='service'),
    url(r'^staff/$', StaffListAdd.as_view(), name='staff'),
    url(r'^absence/$', AbsenceListAdd.as_view(), name='absence'),
    url(r'^holiday/$', HolidayListAdd.as_view(), name='holiday'),
    url(r'^haircut/$', HaircutList.as_view(), name='haircut'),
    url(r'^service/edit/(?P<pk>[0-9]+)/$', ServiceEditDelete.as_view(), name='service-edit'),
    url(r'^staff/edit/(?P<pk>[0-9]+)/$', StaffEditDelete.as_view(), name='staff-edit'),
    url(r'^absence/edit/(?P<pk>[0-9]+)/$', AbsenceEditDelete.as_view(), name='absence-edit'),
    url(r'^holiday/edit/(?P<pk>[0-9]+)/$', HolidayEditDelete.as_view(), name='holiday-edit'),
    url(r'^haircut/delete/(?P<pk>[0-9]+)/$', HaircutDelete.as_view(), name='haircut-delete'),
]