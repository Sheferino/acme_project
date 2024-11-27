from django.db import models
from django.urls import reverse
from .validators import real_age


class Birthday(models.Model):
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField(
        'Фамилия', blank=True, help_text='Необязательное поле', max_length=20
    )
    birthday = models.DateField(
        verbose_name='Дата рождения',
        validators=(real_age,)
    )
    image = models.ImageField(blank=True, verbose_name='Фото',
                              upload_to='birtday_images')

    class Meta:
        verbose_name = 'Запись о ДР'
        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name'),
                name='Unique name',
            ),
        )

    # метод для получения адреса с детальной инфомрацией о записи
    # сюда будет автоматический редирект с CBV, если не указано иное
    def get_absolute_url(self):
        # С помощью функции reverse() возвращаем URL объекта.
        return reverse('birthday:detail', kwargs={'pk': self.pk})

