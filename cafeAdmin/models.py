from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Cafe(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    cafe_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=50, unique=True)
    address = models.TextField(max_length=50)
    unique_link = models.URLField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    qr_code = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.cafe_name

    def get_absolute_url(self):
        return reverse('cafe_menu', kwargs={'slug': self.slug})



