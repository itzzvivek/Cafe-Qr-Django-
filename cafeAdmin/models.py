from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='menu_images', blank=True)
    max_price = models.DecimalField(max_digits=5, decimal_places=2)
    min_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items', default="")

    def __str__(self):
        return self.name
