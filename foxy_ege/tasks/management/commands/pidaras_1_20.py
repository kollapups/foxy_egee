import json
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Manually update tasks 1-20 from tasks_data_svg.json using direct SQL"

    def add_arguments(self, parser):
        parser.add_argument(
            "json_file", type=str, help="Path to the JSON file containing SVG task data"
        )

    def handle(self, *args, **options):
        json_file = options["json_file"]

        # Чтение JSON-файла
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.stdout.write(f"Loaded {len(data)} tasks from {json_file}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to read JSON file: {str(e)}"))
            return

        # Фильтрация задач tasks.task с pk=1–20
        tasks_to_update = [
            task for task in data
            if task.get("model") == "tasks.task" and task.get("pk", 0) in range(1, 21)
        ]
        self.stdout.write(f"Found {len(tasks_to_update)} tasks with model=tasks.task and pk=1–20")

        if not tasks_to_update:
            self.stdout.write(self.style.ERROR("No tasks found for pk=1–20 with model=tasks.task"))
            return

        # Обновление задач
        updated_tasks = 0
        failed_tasks = []

        for task_data in tasks_to_update:
            try:
                task_id = task_data.get("pk")
                fields = task_data.get("fields", {})
                text_svg = fields.get("text_svg")
                solution_text_svg = fields.get("solution_text_svg")
                latex_formula_svg = fields.get("latex_formula_svg")

                self.stdout.write(f"Processing task {task_id}:")
                self.stdout.write(f"  text_svg length: {len(text_svg) if text_svg else 0}")
                self.stdout.write(f"  solution_text_svg length: {len(solution_text_svg) if solution_text_svg else 0}")
                self.stdout.write(f"  latex_formula_svg: {'present' if latex_formula_svg else 'null'}")

                if not solution_text_svg:
                    self.stdout.write(self.style.WARNING(f"  Warning: solution_text_svg is empty for task {task_id}"))
                    failed_tasks.append(task_id)
                    continue

                # Прямое обновление через SQL
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE tasks_task SET text_svg = %s, solution_text_svg = %s, latex_formula_svg = %s WHERE id = %s",
                        [text_svg, solution_text_svg, latex_formula_svg, task_id]
                    )
                    self.stdout.write(f"  Direct SQL update executed for task {task_id}")

                # Проверка результата
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT LENGTH(solution_text_svg) FROM tasks_task WHERE id = %s",
                        [task_id]
                    )
                    result = cursor.fetchone()
                    svg_length = result[0] if result else None
                    self.stdout.write(f"  After SQL update - solution_text_svg length: {svg_length if svg_length else 'NULL'}")

                    if svg_length != len(solution_text_svg) if solution_text_svg else 0:
                        self.stdout.write(self.style.ERROR(f"  Mismatch in solution_text_svg for task {task_id}"))
                        failed_tasks.append(task_id)
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Successfully updated task {task_id}"))
                        updated_tasks += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing task {task_id}: {str(e)}"))
                failed_tasks.append(task_id)
                continue

        # Финальная проверка базы данных
        self.stdout.write("Final database check for tasks 1–20...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, LENGTH(solution_text_svg) FROM tasks_task WHERE id <= 20")
            results = cursor.fetchall()
            for task_id, svg_length in results:
                self.stdout.write(f"Task {task_id}: solution_text_svg length = {svg_length if svg_length else 'NULL'}")

        self.stdout.write(self.style.SUCCESS(f"Update completed: {updated_tasks} tasks updated, {len(failed_tasks)} tasks failed"))
        if failed_tasks:
            self.stdout.write(self.style.WARNING(f"Failed tasks: {failed_tasks}"))