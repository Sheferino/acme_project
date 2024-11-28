from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from .models import Birthday


MAMBETS = ['Серик Берик', 'Саке Баке']


class BirthdayForm(forms.ModelForm):
    class Meta:
        model = Birthday
        fields = '__all__'
        widgets = {'birthday': forms.DateInput(attrs={'type': 'date'})}

    def clean_first_name(self):
        """Функция очистки имени при приёме формы.
        Оставляет только первое имя.

        :return: _description_
        :rtype: _type_
        """
        new_first_name = self.cleaned_data['first_name'].split()[0]
        return new_first_name

    def clean(self):
        """Функция для очистки данных формы.
        Проверяет, чтобы полное имя не было в списке запрещённых

        :raises ValidationError: _description_
        """
        super().clean()
        # Получаем имя и фамилию из очищенных полей формы.
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        # Проверяем вхождение сочетания имени и фамилии во множество имён.
        if f'{first_name} {last_name}' in MAMBETS:
            # отправляем email с ябедой администратору
            send_mail(
                subject="Снова мамбет",
                message=f"{first_name} {last_name} пытался опубликовать запись!",
                from_email="birtday_form@acme.org",
                recipient_list=['admin@acme.org',],
                fail_silently=True
            )

            # поднимаем ошибку валидации всей формы
            raise ValidationError(
                'Мы тоже любим калбитов, но введите, пожалуйста, настоящее имя!'
            )
