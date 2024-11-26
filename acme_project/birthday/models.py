from django.db import models
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

    class Meta:
        verbose_name = 'Запись о ДР'
        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name'),
                name='Unique name',
            ),
        )
