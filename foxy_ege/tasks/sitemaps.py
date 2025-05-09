from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from tasks.models import Task, ExamSubject

class TaskSitemap(Sitemap):
    changefreq = "weekly"  # Задания обновляются еженедельно
    priority = 0.8  # Средний приоритет

    def items(self):
        # Возвращаем все задания
        return Task.objects.all()

    def location(self, obj):
        # URL для задания: /tasks/<subject>/<id>/
        return f"/tasks/{obj.subject}/{obj.id}/"

    def lastmod(self, obj):
        # Если есть поле updated_at, используем его. Иначе возвращаем None
        return getattr(obj, 'updated_at', None)

class SubjectStaticSitemap(Sitemap):
    changefreq = "monthly"  # Статические страницы реже обновляются
    priority = 0.9  # Высокий приоритет для главных страниц

    def items(self):
        # Создаем список кортежей: (имя URL, предмет)
        pages = []
        for subject in ExamSubject:
            pages.extend([
                ('tasks:subject_home', subject.value),
                ('tasks:task_list', subject.value),
                ('tasks:generate_variant', subject.value),
                ('tasks:generate_task', subject.value),
            ])
        return pages

    def location(self, item):
        url_name, subject = item
        return reverse(url_name, kwargs={'subject': subject})

class GlobalStaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        # Статические страницы, не зависящие от предмета
        return ['privacy_policy']

    def location(self, item):
        return reverse(item)