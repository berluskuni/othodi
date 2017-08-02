from django.db import models
from account.models import User


class Date(models.Model):
    data = models.DateField(auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return '%s' % self.data

    def get_date(self):
        return self.data.strftime('%x')

    def get_short_day(self):
        return self.data.strftime('%a')

    def get_data_wik(self):
        return '%s : %s' % (self.data, self.data.strftime('%A'))


class VGarbage(models.Model):
    garbage = models.PositiveSmallIntegerField(default=0, verbose_name='Обьем мусора', blank=True, null=True)
    ordering = models.PositiveSmallIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return '%s' % self.garbage


class TimeInterval(models.Model):
    class Meta:
        ordering = ['ordering']

    time_interval = models.CharField(max_length=18, verbose_name=u'Интервал возможного забора мусора',
                                     blank=True, null=True)
    ordering = models.PositiveSmallIntegerField(default=0)
    date_time = models.ManyToManyField('Date', related_name='date_interval', blank=True)

    def __str__(self):
        if self.time_interval:
            return self.time_interval

    def display_data(self):
        return ', '.join([date.get_date() for date in self.date_time.all()])

    display_data.short_description = 'Date_time'
    display_data.allow_tags = True


class Place(models.Model):
    first_name = models.CharField(max_length=50, verbose_name=u'Имя', blank=True, null=True)
    last_name = models.CharField(max_length=50, verbose_name=u'Фамилия', blank=True, null=True)
    address = models.CharField(max_length=250, verbose_name=u'Адрес заказчика')
    email = models.EmailField(default='')
    phone = models.CharField(max_length=25, verbose_name=u'Телефон', blank=True, null=True)
    v_garbage = models.ForeignKey(VGarbage, related_name='v_garbage', null=True, blank=True)
    latitude = models.FloatField("Latitude", blank=True, null=True,
                                 help_text="degrees, floating point, South is negative")
    longitude = models.FloatField("Longtitude", blank=True, null=True,
                                  help_text="degrees, floating point, West is negative")
    postal_code = models.CharField("Postal Code", blank=True, null=True, max_length=5)
    date = models.ForeignKey(Date, related_name='date', blank=True, null=True)

    def __str__(self):
        try:
            return ' '.join((self.first_name, self.last_name))
        except:
            if self.first_name:
                return self.first_name
            else:
                return "Нет Имени"


class Routes(models.Model):
    class Meta:
        verbose_name_plural = 'Маршруты'
        verbose_name = 'Маршрут'

    title = models.CharField('Маршрут', max_length=50, blank=True, null=True)
    route_place = models.ManyToManyField(Place, related_name='place_route', blank=True)
    ordering = models.PositiveSmallIntegerField(default=0, blank=True, verbose_name='Порядок следования')

    def __str__(self):
        return self.title