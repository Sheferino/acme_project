from django.db import models
from django.urls import reverse
from .validators import real_age
from django.contrib.auth import get_user_model

# получаем модель пользователя. Сделано для возможной смены модели в будущем.
User = get_user_model()


# Личные теги для поздравлений
class Tag(models.Model):
    tag = models.CharField(verbose_name='Тег', max_length=20)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return f'{self.tag}'


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
    author = models.ForeignKey(User, verbose_name='Автор записи',
                               on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        blank=True,
        help_text='Удерживайте ctrl для выбора нескольких вариантов'
    )

    class Meta:
        verbose_name = 'Запись о ДР'
        verbose_name_plural = 'Записи о ДР'
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


# поздравления с ДР
class Congratulation(models.Model):
    text = models.TextField(verbose_name='Текст поздравления')
    birthday = models.ForeignKey(
        Birthday,
        on_delete=models.CASCADE,
        related_name='congratulations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('created_at',)
