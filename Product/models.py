import os

from PIL import Image
from io import BytesIO
from django.core.files import File
from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to="Brands")
    create_at = models.DateTimeField(null=False, blank=False)
    updated_at = models.DateTimeField(null=True, blank=True)
    ref = models.SlugField(null=False, unique=True, blank=True, allow_unicode=True, max_length=120)

    def delete(self, *args, **kwargs):
        ## to delete the image from server
        os.remove(self.image.path)
        super().delete(*args, **kwargs)

    # to compress images need to it
    @staticmethod
    def compress(image, quality=70):
        im = Image.open(image)
        im_io = BytesIO()
        im.save(im_io, 'JPEG', quality=quality)
        new_image = File(im_io, name=image.name)
        return new_image

    def save(self, *args, **kwargs):
        self.ref = slugify(self.name)

        if self.image:
            if self.image.size > (300 * 1024):
                new_image = self.compress(self.image)
                self.image = new_image

        super().save(*args, **kwargs)

    def __str__(self):
        return self.ref


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to="Categories")
    create_at = models.DateTimeField(null=False, blank=False)
    updated_at = models.DateTimeField(null=True, blank=True)
    ref = models.SlugField(null=False, unique=True, blank=True, allow_unicode=True, max_length=120)

    def delete(self, *args, **kwargs):
        ## to delete the image from server
        os.remove(self.image.path)
        super().delete(*args, **kwargs)

    # to compress images need to it
    @staticmethod
    def compress(image, quality=70):
        im = Image.open(image)
        im_io = BytesIO()
        im.save(im_io, 'JPEG', quality=quality)
        new_image = File(im_io, name=image.name)
        return new_image

    def save(self, *args, **kwargs):
        self.ref = slugify(self.name)

        if self.image:
            if self.image.size > (300 * 1024):
                new_image = self.compress(self.image)
                self.image = new_image

        super().save(*args, **kwargs)

    def __str__(self):
        return self.ref


class SubCategory(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    create_at = models.DateTimeField(null=False, blank=False)
    updated_at = models.DateTimeField(null=True, blank=True)
    ref = models.SlugField(null=False, unique=True, blank=True, allow_unicode=True, max_length=120)

    class Meta:
        ordering = ["ref", "create_at", "updated_at"]

    def save(self, *args, **kwargs):
        self.ref = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ref + " -> " + self.category.ref
