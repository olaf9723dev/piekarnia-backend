from django.db import models


class CalendarEvents(models.Model):
    date = models.DateTimeField()
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Święta'
        verbose_name_plural = 'Święta'


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
