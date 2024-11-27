from django.shortcuts import render
from django.views.generic import TemplateView

from birthday.models import Birthday


def homepage(request):
    return render(request, 'pages/index.html')


class HomePage(TemplateView):
    template_name = 'pages/index.html'

    # переопределяем контекст чтобы добавить количество записей
    def get_context_data(self, **kwargs):
        # Получаем словарь контекста из родительского метода.
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь ключ total_count;
        # значение ключа — число объектов модели Birthday.
        context['total_count'] = Birthday.objects.count()
        # Возвращаем изменённый словарь контекста.
        return context
