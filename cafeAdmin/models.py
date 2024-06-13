from django.db import models
from django.urls import reverse


class Cafe(models.Model):
    name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=50, unique=True)
    address = models.TextField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cafe_menu', kwargs={'slug': self.slug})