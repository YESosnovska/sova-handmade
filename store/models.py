import os
import uuid
from PIL import Image
from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=25, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Topic(Tag):
    pass


class Form(Tag):
    pass


def product_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/products/", filename)


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True, upload_to=product_image_file_path)
    size = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    color = models.CharField(max_length=255)
    description = models.TextField(blank=False, null=False)
    topic = models.ForeignKey(
        to=Topic,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="products",
    )
    form = models.ForeignKey(
        to=Form,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="products",
    )
    price = models.PositiveIntegerField(default=0)
    in_stock = models.BooleanField(blank=False, null=False, default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        width, height = img.size

        target_ratio = 3 / 4

        if width / height > target_ratio:
            new_width = int(height * target_ratio)
            left = (width - new_width) // 2
            top = 0
            right = (width + new_width) // 2
            bottom = height
        else:
            new_height = int(width / target_ratio)
            left = 0
            top = (height - new_height) // 2
            right = width
            bottom = (height + new_height) // 2

        img = img.crop((left, top, right, bottom))
        img.save(self.image.path, optimize=True, quality=85)

    def __str__(self):
        return self.name + " - " + self.size
