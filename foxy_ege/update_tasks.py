import json
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_project.settings')  # Замените 'your_project' на имя вашего проекта
django.setup()

from tasks.models import Task  # Предполагается, что ваша модель называется Task

# Загрузите исправленный JSON (можно скопировать его в файл corrected_tasks.json)
with open('corrected_tasks.json', 'r', encoding='utf-8') as f:
    corrected_tasks = json.load(f)

# Обновление записей
for task_data in corrected_tasks:
    task_id = task_data['pk']
    solution_text = task_data['fields']['solution_text']
    
    try:
        task = Task.objects.get(id=task_id)
        task.solution_text = solution_text
        task.save()
        print(f"Updated task with id {task_id}")
    except Task.DoesNotExist:
        print(f"Task with id {task_id} not found")

print("Update completed!")