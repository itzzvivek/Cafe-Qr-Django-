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
    slug = models.SlugField(default="False")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=False, null=True)

    def __str__(self):
        return self.nam

    def get_add_to_cart(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart(self):
        return reverse("core:remove-from-cart", kwargs={
            "slug": self.slug
        })


class OrderItem(models.Model):
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.Integerfield(defualt=1)

    def __str__(self):
        return f"(self.quantity) of {self.item.title}"

    def 