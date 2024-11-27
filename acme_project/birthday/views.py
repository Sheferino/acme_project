from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


class BirthdayListView(ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 4


# миксин для сокращения кода
class BirthdayMixin:
    model = Birthday
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'
    success_url = reverse_lazy('birthday:list_cbv')


class BirthdayCreateView(BirthdayMixin, CreateView):
    ''' этот код не нужн в связи с вводом миксина
    model = Birthday
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'
    success_url = reverse_lazy('birthday:list_cbv')'''
    pass


class BirthdayUpdateView(BirthdayMixin, UpdateView):
    pass


class BirthdayDeleteView(DeleteView):
    model = Birthday
    template_name = 'birthday/confirm_delete.html'
    success_url = reverse_lazy('birthday:list_cbv')


def birthday(request, pk=None):
    if not (pk is None):
        instance = get_object_or_404(Birthday, pk=pk)
    else:
        instance = None
    form = BirthdayForm(request.POST or None,
                        files=request.FILES or None,
                        instance=instance)
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
    # настраиваем пагинатор
    paginator = Paginator(bd_list, 3)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    # готовим данные для передачи в шаблон
    # отдаём список записей для отображения и объект страницы пагинатора
    context = {'birthday_list': page_obj, 'page_obj':page_obj}
    return render(request, template, context)


def delete_birthday(request, pk):
    # Получаем объект модели или выбрасываем 404 ошибку.
    instance = get_object_or_404(Birthday, pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    # Если был получен POST-запрос...
    if request.method == 'POST':
        # ...удаляем объект:
        instance.delete()
        # ...и переадресовываем пользователя на страницу со списком записей.
        return redirect('birthday:list')
    # Если был получен GET-запрос — отображаем форму.
    return render(request, 'birthday/birthday.html', context)
