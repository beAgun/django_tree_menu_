from django.db import models
from django.urls import reverse


class Menu(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Слаг')
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE,
                               null=True, blank=True,
                               related_name='children',
                               verbose_name='Родитель')
    root = models.CharField(max_length=255, verbose_name='Корень/название меню')
    path = models.URLField(verbose_name='Путь')

    objects = models.Manager

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('menu_item', kwargs={'menu_item_path': self.path})

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        print(self, self.parent)
        if self.parent is None:
            self.root = self.name
            self.path = self.slug

        else:
            self.root = self.parent.root
            self.path = self.parent.path + self.slug

        super(Menu, self).save()
