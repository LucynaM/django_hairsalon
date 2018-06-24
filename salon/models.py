from django.db import models

from django.contrib.auth.models import AbstractUser


STATUSES = (
    (1, 'reserved'),
    (2, 'confirmed')
)
DURATION = (
    (60, '1h'),
    (120, '2h'),
    (180, '3h'),
    (240, '4h'),
)


class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.IntegerField(unique=True, verbose_name='Telefon')
    about = models.TextField(null=True, blank=True, verbose_name='Opis')

    REQUIRED_FIELDS = ['email', 'phone']

    @property
    def name(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        if self.name:
            return self.name
        return self.username


class NonOnlineCustomer(models.Model):
    name = models.CharField(max_length=60, verbose_name='Imię i nazwisko')
    phone = models.IntegerField(verbose_name='Telefon')


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nazwa')
    price = models.FloatField(verbose_name='Cena')
    duration = models.IntegerField(choices=DURATION, verbose_name='Czas trwania')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='Opis')

    def __str__(self):
        return self.name


class Haircut(models.Model):
    service = models.ForeignKey(Service, related_name='haircuts', on_delete=models.SET_NULL, null=True, verbose_name='Usługa')
    staff = models.ForeignKey(MyUser, related_name='services', on_delete=models.SET_NULL, null=True, verbose_name='Fryzjer')
    customer = models.ForeignKey(MyUser, related_name='haircuts', on_delete=models.CASCADE, verbose_name='Klient')
    date = models.DateTimeField(verbose_name='Data')
    status = models.IntegerField(choices=STATUSES, default=1, verbose_name='Status')
    info = models.CharField(max_length=255, null=True, blank=True, verbose_name='Informacje')
    non_online_customer = models.ForeignKey(NonOnlineCustomer, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return '{}: {}'.format(self.staff.name or self.staff.username, self.date.strftime('%d.%m.%Y %H:%M'))


class Absence(models.Model):
    start = models.DateField(verbose_name='Początek')
    end = models.DateField(verbose_name='Koniec')
    staff = models.ForeignKey(MyUser, related_name='absences', on_delete=models.CASCADE, verbose_name='Pracownik')

    def __str__(self):
        return '{}: {}-{}'.format(self.staff.name or self.staff.username, self.start.strftime('%d.%m.%Y'), self.end.strftime('%d.%m.%Y'))


class Holiday(models.Model):
    day = models.DateField(verbose_name='Dzień')

    def __str__(self):
        return self.day.strftime('%d.%m.%Y')


class Comment(models.Model):
    comment = models.TextField()
    haircut = models.ForeignKey(Haircut, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)


