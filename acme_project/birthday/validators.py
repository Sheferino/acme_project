from datetime import date
from django.core.exceptions import ValidationError


def real_age(value: date) -> None:
    # Считаем разницу между сегодняшним днём и днём рождения в днях
    # и делим на 365.
    age = (date.today() - value).days / 365
    # Если возраст меньше 1 года или больше 120 лет — выбрасываем ошибку.
    if age < 1 or age > 120:
        raise ValidationError(
            'Ожидается возраст от 1 года до 120 лет'
        )
