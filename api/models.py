from django.db import models
from django.utils.text import slugify
from django.utils import timezone

#  ?  chủ đề
class Topic(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True , null=True)
    
    class Meta:
        # ordering = ['-updated_at', '-created_at']
        ordering = ['-created_at', '-updated_at']
    
    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        if not self.slug:
            base_slug = slugify(self.title)  # Chuyển name thành slug cơ bản
            slug = base_slug
            counter = 1
            while Topic.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"  # Thêm số vào slug nếu bị trùng
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

#  ? Thể loại    
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True , null=True)
    
    class Meta:
        # ordering = ['-updated_at', '-created_at']
        ordering = ['-created_at', '-updated_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)  # Chuyển name thành slug cơ bản
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"  # Thêm số vào slug nếu bị trùng
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# ? Quốc gia
class Country(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True , null=True)
    
    class Meta:
        # ordering = ['-updated_at', '-created_at']
        ordering = ['-created_at', '-updated_at']
    
    def save(self, *args, **kwargs):
        # if not self.slug:
        base_slug = slugify(self.name)  # Chuyển name thành slug cơ bản
        slug = base_slug
        counter = 1
        while Country.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"  # Thêm số vào slug nếu bị trùng
            counter += 1
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    