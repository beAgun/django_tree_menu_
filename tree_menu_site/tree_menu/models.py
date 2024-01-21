from django.db import models
from django.urls import reverse


# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE,
                               null=True, blank=True,
                               related_name='children',
                               verbose_name='Родитель')

    objects = models.Manager

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('menu_item', kwargs={'menu_item_path': self.slug})