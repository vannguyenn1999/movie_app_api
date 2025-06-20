from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from api.models import Topic, Category, Country
from actor.models import Actor

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    rating = models.FloatField(max_length=3, default=0.0)
    imdb = models.FloatField(max_length=3, default=0.0)
    duration = models.CharField(max_length=10, default='0')
    image = models.ImageField(_("Movie_Image"),upload_to='movies/thumbs/', null=True, blank=True)
    image_avatar = models.ImageField(_("Movie_Image_Avatar"),upload_to='movies/avatar/', null=True, blank=True)
    video = models.FileField(_("Videos"),upload_to='videos/', null=True, blank=True , max_length=255)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    language = models.CharField(max_length=10, default='English')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Hiển thị nên banner ở header
    is_banner = models.BooleanField(default=False)

    # Hiển thị ở trang quảng cáo
    is_ads = models.BooleanField(default=False)
    
    category = models.ManyToManyField(Category, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    actor = models.ManyToManyField(Actor, blank=True)
    topic = models.ManyToManyField(Topic, blank=True)
    
    class Meta:
        # ordering = ['-updated_at', '-created_at']
        ordering = ['-created_at', '-updated_at']
    
    
    def save(self, *args, **kwargs):
        # if not self.slug:
        base_slug = slugify(self.title)  # Chuyển name thành slug cơ bản
        slug = base_slug
        counter = 1
        while Movie.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"  # Thêm số vào slug nếu bị trùng
            counter += 1
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class TopMovie(models.Model):
    movie = models.ForeignKey(Movie ,on_delete=models.CASCADE, blank=True, null=True)
    level = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering = ['-updated_at', '-created_at']
        ordering = ['level']