from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

# Create your models here.
class CustomUser(AbstractUser):
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='imgs/profiles', null=True)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)