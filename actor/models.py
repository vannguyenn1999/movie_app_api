from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


# diễn viên
class Actor(models.Model):
    
    options = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Diff', 'Diff') ,
    )
    
    name = models.CharField(max_length=255)
    info = models.TextField()
    image = models.ImageField(_("Actor_Image"),upload_to='actor', null=True, blank=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=options, default='Nam')
    slug = models.SlugField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True , null=True)
    
    def save(self, *args, **kwargs):
        # if not self.slug:
        base_slug = slugify(self.name)  # Chuyển name thành slug cơ bản
        slug = base_slug
        counter = 1
        while Actor.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"  # Thêm số vào slug nếu bị trùng
            counter += 1
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    