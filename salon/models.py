from django.db import models
from django.urls import reverse
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
    phone = models.IntegerField(unique=True)
    about = models.TextField(null=True, blank=True)

    REQUIRED_FIELDS = ['email', 'phone']

    def get_absolute_url(self):
        return reverse('salon:user-detail', kwargs={'pk': self.pk})

    @property
    def name(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        if self.name:
            return self.name
        return self.username


class Service(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    duration = models.IntegerField(choices=DURATION)
    description = models.CharField(max_length=255, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('salon:service-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Haircut(models.Model):
    service = models.ForeignKey(Service, related_name='haircuts', on_delete=models.SET_NULL, null=True)
    staff = models.ForeignKey(MyUser, related_name='services', on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(MyUser, related_name='haircuts', on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.IntegerField(choices=STATUSES, default=1)
    info = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '{}: {}'.format(self.staff.name, self.date.strftime('%d.%m.%Y %H:%M'))


class Absence(models.Model):
    start = models.DateField()
    end = models.DateField()
    staff = models.ForeignKey(MyUser, related_name='absences', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('salon:absence-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{}: {}-{}'.format(self.staff.name or self.staff.username, self.start.strftime('%d.%m.%Y'), self.end.strftime('%d.%m.%Y'))


class Holiday(models.Model):
    day = models.DateField()

    def get_absolute_url(self):
        return reverse('salon:holiday-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.day.strftime('%d.%m.%Y')


class Comment(models.Model):
    comment = models.TextField()
    haircut = models.ForeignKey(Haircut, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)

