from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


# миксин для сокращения кода
class BirthdayMixin:
    model = Birthday
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'


class BirthdayListView(ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 4


class BirthdayDetailView(DetailView):
    model = Birthday
    template_name = 'birthday/detail.html'

    # переопределяем функцию получения контекста,
    # чтобы в ней рассчитать количество дней до ДР
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        return context


class BirthdayCreateView(LoginRequiredMixin, BirthdayMixin, CreateView):
    ''' этот код не нужен в связи с вводом миксина
    model = Birthday
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'''
    success_url = reverse_lazy('birthday:list_cbv')

    # переопределяем валидация формы для добавления автора записи
    def form_valid(self, form):
        # добавляем в экземпляр формы автора
        form.instance.author = self.request.user
        # продолжаем валидацию
        return super().form_valid(form)


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
        # сохраняем экземпляр формы без сохранения в БД
        instance = form.save(commit=False)
        # добавляем в него пользователя
        instance.author = request.user
        # сохраняем экземпляр в БД
        instance.save()
        # вызоваем функцию подсчёта дней:
        birthday_countdown = calculate_birthday_countdown(
            form.cleaned_data['birthday']
        )
        # Обновляем словарь контекста: добавляем в него новый элемент.
        context['countdown'] = birthday_countdown
    return render(request, 'birthday/birthday.html', context)

@login_required
def birthday_list(request):
    template = 'birthday/birthday_list.html'
    bd_list = Birthday.objects.all().order_by('last_name')
    # настраиваем пагинатор
    paginator = Paginator(bd_list, 3)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    # готовим данные для передачи в шаблон
    # отдаём список записей для отображения и объект страницы пагинатора
    context = {'birthday_list': page_obj, 'page_obj': page_obj}
    return render(request, template, context)


def delete_birthday(request, pk):
    # Получаем объект модели или выбрасываем 404 ошибку. Проверяем авторство
    instance = get_object_or_404(Birthday, pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    # Если был получен POST-запрос...
    if request.method == 'POST':
        if instance.author==request.user:
            # удаляем объект:
            instance.delete()
            # и переадресовываем пользователя на страницу со списком записей.
            return redirect('birthday:list')
        else:
            return redirect('registration')
    # Если был получен GET-запрос — отображаем форму.
    return render(request, 'birthday/birthday.html', context)
