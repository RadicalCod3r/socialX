from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Status(models.Model):
    status_text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='imgs/media', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(
        get_user_model(),
        related_name='favorites'
    )
    creator = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='status_list'
    )
    retweet_on = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='retweets',
        null=True
    )
    reply_on = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        null=True
    )

    class Meta:
        verbose_name_plural = 'Status List'

    def __str__(self):
        return self.status_text

    # def get_absolute_url(self):
