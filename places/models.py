from django.contrib.auth.models import User
from django.db import models
from simple_history.models import HistoricalRecords


class Place(models.Model):
    class Meta:
        verbose_name = 'Lokal'
        verbose_name_plural = 'Lokale'
    name = models.CharField(max_length=1024)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    address = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=6)
    city = models.CharField(max_length=128)
    logo = models.ImageField()
    description = models.TextField()
    is_enabled = models.BooleanField(default=False)
    enable_date = models.DateField(null=True, blank=True)
    telephone = models.CharField(max_length=16)
    cloud_id = models.CharField(max_length=16, null=True, blank=True)
    refresh_token = models.CharField(max_length=256, null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} ({self.address}, {self.zip_code} {self.city}) - {'włączony' if self.is_enabled else 'wyłączony'}"

    @property
    def image_url(self):
        if self.logo:
            url = self.logo.url
        else:
            url = ''
        return url


class OpeningHours(models.Model):
    class Meta:
        verbose_name = 'Godziny Otwarcia'
        verbose_name_plural = 'Godziny Otwarcia'
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    day_of_week = models.IntegerField()
    start_time = models.TimeField(null=True, blank=True, default='00:00:00.000000')
    end_time = models.TimeField(null=True, blank=True, default='00:00:00.000000')

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.place.name} - {self.day_of_week} - {self.start_time}:{self.end_time}"

    # @property
    # def start_time(self):
    #     return '%s:%s' % (self.start_time.strftime('%H:%M'))

    @property
    def day_of_week_in_polish(self):
        if self.day_of_week == 1:
            return 'Poniedziałek'
        elif self.day_of_week == 2:
            return 'Wtorek'
        elif self.day_of_week == 3:
            return 'Środa'
        elif self.day_of_week == 4:
            return 'Czwartek'
        elif self.day_of_week == 5:
            return 'Piątek'
        elif self.day_of_week == 6:
            return 'Sobota'
        else:
            return 'Niedziela'

    @property
    def day_in_english(self):
        if self.day_of_week == 1:
            return 'monday'
        elif self.day_of_week == 2:
            return 'tuesday'
        elif self.day_of_week == 3:
            return 'wednesday'
        elif self.day_of_week == 4:
            return 'thursday'
        elif self.day_of_week == 5:
            return 'friday'
        elif self.day_of_week == 6:
            return 'saturday'
        else:
            return 'sunday'


class CustomOpeningHours(models.Model):
    class Meta:
        verbose_name = 'Niestandardowe Godziny Otwarcia'
        verbose_name_plural = 'Niestandardowe Godziny Otwarcia'

    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.place.name} - {self.date} - {self.is_closed} - {self.start_time}:{self.end_time}"


class PlaceReview(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.FloatField()
    date = models.DateTimeField()
    is_accepted = models.BooleanField(default=False)
    comment = models.TextField()

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.place.name} - {self.author.username} - {self.date} - {self.is_accepted} - {self.rate}"
