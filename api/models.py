from django.db import models

# Create your models here.


class Topic(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True , null=True)

    def __str__(self):
        return self.title
    
class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True , null=True)

    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True , null=True)

    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True , null=True)

    def __str__(self):
        return self.name
    