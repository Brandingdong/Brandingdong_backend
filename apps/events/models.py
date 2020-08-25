from django.db import models

# Create your models here.

class Events(models.Model):
    images = models.ImageField(upload_to='events', verbose_name='이벤트이미지')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '이벤트'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']
