from django.conf.urls import url
from .views import ServiceCreate, ServiceDelete, ServiceDetail, ServiceList, ServiceUpdate, \
    AbsenceCreate, AbsenceDelete, AbsenceDetail, AbsenceList, AbsenceUpdate, \
    HolidayCreate, HolidayDelete, HolidayDetail, HolidayList, HolidayUpdate, \
    CustomerCreate, CustomerUpdate, StaffList, StaffUpdate, StaffCreate, UserDelete, UserDetail, \
    LoginView, logout_user, SearchView, ReservationView, \
    MainPage

urlpatterns = [
    url(r'^services/?$', ServiceList.as_view(), name='service-list'),
    url(r'^services/(?P<pk>[0-9]+)/$', ServiceDetail.as_view(), name='service-detail'),
    url(r'^services/add/$', ServiceCreate.as_view(), name='service-add'),
    url(r'^services/edit/(?P<pk>[0-9]+)/$', ServiceUpdate.as_view(), name='service-edit'),
    url(r'^services/delete/(?P<pk>[0-9]+)/$', ServiceDelete.as_view(), name='service-delete'),
    url(r'^absences/?$', AbsenceList.as_view(), name='absence-list'),
    url(r'^absences/(?P<pk>[0-9]+)/$', AbsenceDetail.as_view(), name='absence-detail'),
    url(r'^absences/add/$', AbsenceCreate.as_view(), name='absence-add'),
    url(r'^absences/edit/(?P<pk>[0-9]+)/$', AbsenceUpdate.as_view(), name='absence-edit'),
    url(r'^absences/delete/(?P<pk>[0-9]+)/$', AbsenceDelete.as_view(), name='absence-delete'),
    url(r'^holidays/?$', HolidayList.as_view(), name='holiday-list'),
    url(r'^holidays/(?P<pk>[0-9]+)/$', HolidayDetail.as_view(), name='holiday-detail'),
    url(r'^holidays/add/$', HolidayCreate.as_view(), name='holiday-add'),
    url(r'^holidays/edit/(?P<pk>[0-9]+)/$', HolidayUpdate.as_view(), name='holiday-edit'),
    url(r'^holidays/delete/(?P<pk>[0-9]+)/$', HolidayDelete.as_view(), name='holiday-delete'),
    url(r'^staff/$', StaffList.as_view(), name='myuser-list'),
    url(r'^user/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='myuser-detail'),
    url(r'^staff/add/$', StaffCreate.as_view(), name='staff-add'),
    url(r'^staff/edit/(?P<pk>[0-9]+)/$', StaffUpdate.as_view(), name='staff-edit'),
    url(r'^user/delete/(?P<pk>[0-9]+)/$', UserDelete.as_view(), name='myuser-delete'),
    url(r'^customer/add/$', CustomerCreate.as_view(), name='customer-add'),
    url(r'^customer/edit/(?P<pk>[0-9]+)/$', CustomerUpdate.as_view(), name='customer-edit'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^reserve/(?P<date>([a-zA-Z0-9\-:])+)/(?P<user>(\d)+)/(?P<service_id>(\d)+)/$', ReservationView.as_view(),
        name='reservation'),
    # new urls
    url(r'^main/$', MainPage.as_view(), name='main'),
]