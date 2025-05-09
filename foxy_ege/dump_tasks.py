# dump_tasks.py
import os
import json
from django.core.management import call_command
from django.core.serializers import serialize
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
    Favorite,
)


def dump_tasks():
    # Список моделей для сериализации
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
        Favorite,
    ]

    # Сериализуем данные
    data = []
    for model in models:
        data.extend(serialize("json", model.objects.all()))

    # Записываем в файл с UTF-8
    with open("tasks_backup.json", "w", encoding="utf-8") as f:
        json.dump(
            json.loads("[" + ",".join(data) + "]"), f, ensure_ascii=False, indent=2
        )


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foxy_ege.settings")
    import django

    django.setup()
    dump_tasks()
