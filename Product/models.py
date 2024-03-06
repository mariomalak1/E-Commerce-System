import datetime
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
    created_at = models.DateTimeField(null=False, blank=False)
    updated_at = models.DateTimeField(null=True, blank=True)
    ref = models.SlugField(null=False, unique=True, blank=True, allow_unicode=True, max_length=120)

    class Meta:
        ordering = ["ref", "created_at", "updated_at"]

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
    created_at = models.DateTimeField(null=False, blank=False)
    updated_at = models.DateTimeField(null=True, blank=True)
    ref = models.SlugField(null=False, unique=True, blank=True, allow_unicode=True, max_length=120)

    class Meta:
        ordering = ["ref", "created_at", "updated_at"]

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
    created_at = models.DateTimeField(null=False, blank=False)
    updated_at = models.DateTimeField(null=True, blank=True)
    ref = models.SlugField(null=False, unique=True, blank=True, allow_unicode=True, max_length=120)

    class Meta:
        ordering = ["ref", "created_at", "updated_at"]

    def save(self, *args, **kwargs):
        self.ref = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ref + " -> " + self.category.ref

class Product(models.Model):
    def uploadProductCoverImagePath(self, filename):
        return "Products\\" + "\\" + self.product.title + "\\Cover"

    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=False)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=False)
    rating = models.DecimalField(default=0, max_digits=5, decimal_places=1)
    created_at = models.DateTimeField(null=False, blank=False)
    updated_at = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)
    imageCover = models.ImageField(upload_to=uploadProductCoverImagePath, null=False, blank=False)
    ref = models.CharField(max_length=500, null=False, blank=False)

    class Meta:
        ordering = ["ref", "created_at", "updated_at"]


    # function that try to return unique fields to
    def __getFieldsOfModelToSlugify(self, counter = 0):
        if counter == 0:
            return self.title
        elif counter == 1:
            return self.title + " " + self.created_at.second + " " + self.created_at.min
        elif counter == 2:
            return self.title + " " + self.created_at.second + "" + self.created_at.min + self.created_at.hour
        elif counter == 3:
            return self.title + " " + self.created_at.second + "" + self.created_at.min + self.created_at.hour + self.created_at.day
        elif counter == 4:
            return self.title + " " + self.created_at.second + "" + self.created_at.min + self.created_at.hour + self.created_at.day + self.created_at.month + self.created_at.year

    def save(self, *args, **kwargs):
        self.created_at = datetime.datetime.now()

        # to make unique slugify to ref
        counter = 0
        while (counter + 1):
            self.ref = slugify(self.__getAllFieldsOfModel())
            product = Product.objects.filter(ref=self.ref).first()
            if product:
                counter += 1
            else:
                counter = -1

        # check on the image if it's big will compress it
        if self.image:
            if self.image.size > (300 * 1024):
                new_image = self.compress(self.image)
                self.image = new_image

        super().save(*args, **kwargs)

    # to compress images need to it
    @staticmethod
    def compress(image, quality=90):
        im = Image.open(image)
        im_io = BytesIO()
        im.save(im_io, 'JPEG', quality=quality)
        new_image = File(im_io, name=image.name)
        return new_image

    def delete(self, *args, **kwargs):
        ## to delete the image from server
        os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.ref

class Productmages(models.Model):
    def uploadToPath(self, filename):
        return "Products\\" + "\\" + self.product.title + "\\images"

    image = models.ImageField(upload_to=uploadToPath)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        # check on the image if it's big will compress it
        if self.image:
            if self.image.size > (300 * 1024):
                new_image = self.compress(self.image)
                self.image = new_image

        super().save(*args, **kwargs)

    # to compress images need to it
    @staticmethod
    def compress(image, quality=90):
        im = Image.open(image)
        im_io = BytesIO()
        im.save(im_io, 'JPEG', quality=quality)
        new_image = File(im_io, name=image.name)
        return new_image

    def delete(self, *args, **kwargs):
        ## to delete the image from server
        os.remove(self.image.path)
        super().delete(*args, **kwargs)