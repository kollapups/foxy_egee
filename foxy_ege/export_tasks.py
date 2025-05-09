import os
import sys
import django
import json
import argparse
from django.db.models.fields.files import ImageField
from django.db.models import ForeignKey, DateTimeField, DateField

# Добавляем корень проекта в sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Настройка окружения Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "new_project.settings")
django.setup()

from tasks.models import (
    Task,
    ExamPart,
    ExamLine,
    Topic,
    Subtopic,
    Source,
    SolutionImage,
    Comment,
    GeneratedVariant,
)

# Список моделей для экспорта
models = [
    Task,
    ExamPart,
    ExamLine,
    Topic,
    Subtopic,
    Source,
    SolutionImage,
    Comment,
    GeneratedVariant,
]

def export_tasks(task_ids=None, task_range=None):
    data = []
    for model in models:
        # Фильтруем задачи по task_ids или task_range
        if model == Task:
            if task_ids:
                # Экспорт конкретных задач по unique_id
                objects = model.objects.filter(unique_id__in=task_ids)
                print(f"Экспортируются задачи с unique_id: {task_ids}")
            elif task_range:
                # Экспорт задач в диапазоне (например, 130-150)
                start, end = task_range
                objects = model.objects.filter(unique_id__gte=start, unique_id__lte=end)
                print(f"Экспортируются задачи с unique_id от {start} до {end}")
            else:
                # Экспорт всех задач
                objects = model.objects.all()
                print("Экспортируются все задачи")
        else:
            objects = model.objects.all()

        for obj in objects:
            fields = {}
            for field in model._meta.fields:
                value = getattr(obj, field.name)
                if isinstance(field, ImageField):
                    fields[field.name] = str(value) if value else None
                elif isinstance(field, ForeignKey):
                    fields[field.name] = value.pk if value else None
                elif isinstance(field, (DateTimeField, DateField)):
                    fields[field.name] = value.isoformat() if value else None
                else:
                    fields[field.name] = value
            data.append(
                {"model": f"tasks.{model.__name__.lower()}", "pk": obj.pk, "fields": fields}
            )

    # Сохранение в файл с UTF-8
    with open("tasks_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Экспортировано {len(data)} записей в tasks_data.json")

if __name__ == "__main__":
    # Настройка аргументов командной строки
    parser = argparse.ArgumentParser(description="Экспорт задач в JSON для рендеринга")
    parser.add_argument(
        "--range",
        nargs=2,
        type=str,
        metavar=("START", "END"),
        help="Диапазон unique_id для экспорта (например, 130 150)"
    )
    parser.add_argument(
        "--ids",
        nargs="+",
        type=str,
        help="Список unique_id для экспорта (например, 151 159 164)"
    )

    args = parser.parse_args()

    if args.range and args.ids:
        print("Ошибка: укажите либо --range, либо --ids, но не оба сразу")
        sys.exit(1)

    if args.range:
        start, end = args.range
        export_tasks(task_range=(start, end))
    elif args.ids:
        export_tasks(task_ids=args.ids)
    else:
        export_tasks()  # Экспорт всех задач