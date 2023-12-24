from django.db import models

# Create your models here.
class Complement(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок'
    )
    
    def __str__(self):
        return self.title 
    
    @classmethod
    def get_random(cls):
        return cls.objects.order_by('?').first()

    class Meta:
        verbose_name = 'Комплемент'
        verbose_name_plural = 'комплементы'

class Photo(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок к фотографии',
        blank=True, null=True
    )
    image = models.ImageField(
        upload_to='photos/',
        verbose_name="Фотография"
    )

    def __str__(self):
        return self.title 
    
    @classmethod
    def get_random(cls):
        return cls.objects.order_by('?').first()
    
    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'

class Movie(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название фильма"
    )
    watched = models.BooleanField(
        default=False,
        verbose_name="Смотрел"
    )

    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"