from django.db import models
from django.contrib.auth.models import User


class URL(models.Model):
    original_url = models.URLField()
    short_alias = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.IntegerField(default=0)

class Click(models.Model):
    url = models.ForeignKey(URL, on_delete=models.CASCADE)
    clicked_at = models.DateTimeField(auto_now_add=True)
    referer = models.URLField(blank=True, null=True)
    ip_address = models.CharField(max_length=200, null=True)
