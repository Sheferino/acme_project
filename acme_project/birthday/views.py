from django.shortcuts import render

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


def birthday(request):
    form = BirthdayForm(request.POST or None)
    # Создаём словарь контекста сразу после инициализации формы.
    context = {'form': form}
    # Если форма валидна...
    if form.is_valid():
        form.save()
        # ...вызовем функцию подсчёта дней:
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
        )
        # Обновляем словарь контекста: добавляем в него новый элемент.
        context['countdown'] = birthday_countdown
    return render(request, 'birthday/birthday.html', context)


def birthday_list(request):
    template = 'birthday/birthday_list.html'
    bd_list = Birthday.objects.all().order_by('last_name')
    context = {'birthday_list': bd_list}
    return render(request, template, context)
