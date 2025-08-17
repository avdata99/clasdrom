from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class RequestLog(models.Model):
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    method = models.CharField(max_length=10)
    url = models.URLField(max_length=500)
    path = models.CharField(max_length=500)
    query_string = models.TextField(blank=True)
    referer = models.URLField(max_length=500, blank=True)
    response_status = models.IntegerField(null=True, blank=True)
    response_time_ms = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Request Log'
        verbose_name_plural = 'Request Logs'

    def __str__(self):
        return f"{self.method} {self.path} - {self.ip_address} at {self.timestamp}"

    @property
    def user_display(self):
        return self.user.username if self.user else 'Anonymous'
