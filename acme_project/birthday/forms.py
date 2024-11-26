from django import forms
from django.core.exceptions import ValidationError
from .models import Birthday


MAMBETS = ['Серик Берик', 'Саке Баке']

class BirthdayForm(forms.ModelForm):
    class Meta:
        model = Birthday
        fields = '__all__'
        widgets = {'birthday': forms.DateInput(attrs={'type': 'date'})}

    def clean_first_name(self):
        new_first_name = self.cleaned_data['first_name'].split()[0]
        return new_first_name
    
    def clean(self):
        # Получаем имя и фамилию из очищенных полей формы.
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        # Проверяем вхождение сочетания имени и фамилии во множество имён.
        if f'{first_name} {last_name}' in MAMBETS:
            raise ValidationError(
                'Мы тоже любим калбитов, но введите, пожалуйста, настоящее имя!'
            ) 
