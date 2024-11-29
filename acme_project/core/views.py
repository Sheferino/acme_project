from django.shortcuts import render


# функция для страницы 404
def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию;
    # выводить её в шаблон пользовательской страницы 404 мы не станем.
    return render(request, 'core/404.html', status=404)


# ошибка проверки csrf
def csrf_failure(request, reason=''):
    return render(request, 'core/403csrf.html', status=403) 