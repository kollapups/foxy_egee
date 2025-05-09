import json
from django.core.management.base import BaseCommand
from django.db import connection
from tasks.models import Task

class Command(BaseCommand):
    help = "Import SVG-rendered task data from JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            "json_file", type=str, help="Path to the JSON file containing SVG task data"
        )
        parser.add_argument(
            "--batch-size", type=int, default=50, help="Number of tasks to process in one batch"
        )

    def handle(self, *args, **options):
        json_file = options["json_file"]
        batch_size = options["batch_size"]

        # Чтение JSON-файла
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.stdout.write(f"Loaded {len(data)} records from {json_file}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to read JSON file: {str(e)}"))
            return

        # Проверка структуры данных
        if not isinstance(data, list):
            self.stdout.write(self.style.ERROR("JSON data must be a list of records"))
            return

        # Фильтрация только записей tasks.task
        task_data_list = [item for item in data if item.get("model") == "tasks.task"]
        self.stdout.write(f"Found {len(task_data_list)} tasks with model=tasks.task")

        if not task_data_list:
            self.stdout.write(self.style.ERROR("No tasks found with model=tasks.task"))
            return

        processed_tasks = 0
        skipped_tasks = 0
        failed_tasks = []

        # Логируем первые 20 задач
        self.stdout.write("First 20 tasks in JSON:")
        for task_data in task_data_list[:20]:
            task_id = task_data.get("pk", "unknown")
            fields = task_data.get("fields", {})
            solution_text_svg = fields.get("solution_text_svg", None)
            latex_formula_svg = fields.get("latex_formula_svg", None)
            has_complex = solution_text_svg and 'class="complex-formula"' in solution_text_svg
            self.stdout.write(
                f"Task {task_id}: solution_text_svg={'present' if solution_text_svg else 'missing'}, "
                f"latex_formula_svg={'present' if latex_formula_svg else 'missing'}, "
                f"has_complex_formula={has_complex}"
            )

        # Обрабатываем задачи
        for i, task_data in enumerate(task_data_list):
            try:
                task_id = task_data.get("pk")
                if not task_id:
                    self.stdout.write(self.style.WARNING(f"Skipping task with missing pk"))
                    skipped_tasks += 1
                    continue

                fields = task_data.get("fields", {})
                text_svg = fields.get("text_svg")
                solution_text_svg = fields.get("solution_text_svg")
                latex_formula_svg = fields.get("latex_formula_svg")

                self.stdout.write(f"Processing task {task_id}:")
                self.stdout.write(f"  text_svg length: {len(text_svg) if text_svg else 0}")
                self.stdout.write(f"  solution_text_svg length: {len(solution_text_svg) if solution_text_svg else 0}")
                self.stdout.write(f"  latex_formula_svg: {'present' if latex_formula_svg else 'null'}")
                self.stdout.write(f"  contains complex-formula: {'yes' if solution_text_svg and 'class=\"complex-formula\"' in solution_text_svg else 'no'}")

                # Поиск существующей задачи
                try:
                    task = Task.objects.get(id=task_id)
                    self.stdout.write(f"  Found existing task with id {task_id}")
                except Task.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"  Task {task_id} not found, skipping"))
                    skipped_tasks += 1
                    failed_tasks.append(task_id)
                    continue

                # Проверка данных перед сохранением
                if not text_svg:
                    self.stdout.write(self.style.WARNING(f"  Warning: text_svg is empty for task {task_id}"))
                if not solution_text_svg:
                    self.stdout.write(self.style.WARNING(f"  Warning: solution_text_svg is empty for task {task_id}"))

                # Обновление полей через ORM
                task.text_svg = text_svg
                task.solution_text_svg = solution_text_svg
                task.latex_formula_svg = latex_formula_svg
                task.save(skip_svg_render=True)

                # Проверка после сохранения через ORM
                task.refresh_from_db()
                self.stdout.write(f"  After ORM save - text_svg length: {len(task.text_svg) if task.text_svg else 0}")
                self.stdout.write(f"  After ORM save - solution_text_svg length: {len(task.solution_text_svg) if task.solution_text_svg else 0}")
                self.stdout.write(f"  After ORM save - latex_formula_svg: {'present' if task.latex_formula_svg else 'null'}")

                if task.solution_text_svg != solution_text_svg:
                    self.stdout.write(self.style.ERROR(f"  Mismatch in solution_text_svg for task {task_id}"))
                    failed_tasks.append(task_id)
                    continue

                # Дополнительное сохранение напрямую в базу
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE tasks_task SET text_svg = %s, solution_text_svg = %s, latex_formula_svg = %s WHERE id = %s",
                        [text_svg, solution_text_svg, latex_formula_svg, task_id]
                    )
                    self.stdout.write(f"  Direct SQL update executed for task {task_id}")

                # Проверка после прямого SQL-запроса
                task.refresh_from_db()
                self.stdout.write(f"  After SQL update - text_svg length: {len(task.text_svg) if task.text_svg else 0}")
                self.stdout.write(f"  After SQL update - solution_text_svg length: {len(task.solution_text_svg) if task.solution_text_svg else 0}")
                self.stdout.write(f"  After SQL update - latex_formula_svg: {'present' if task.latex_formula_svg else 'null'}")

                if task.solution_text_svg != solution_text_svg:
                    self.stdout.write(self.style.ERROR(f"  Mismatch in solution_text_svg after SQL update for task {task_id}"))
                    failed_tasks.append(task_id)
                else:
                    self.stdout.write(self.style.SUCCESS(f"Successfully updated task {task_id}"))
                    processed_tasks += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing task {task_id}: {str(e)}"))
                skipped_tasks += 1
                failed_tasks.append(task_id)
                continue

            # Периодическая проверка базы данных
            if (i + 1) % batch_size == 0:
                self.stdout.write(f"Checking database after {i + 1} tasks...")
                sample_task = Task.objects.filter(id__in=[1, 2, 3]).first()
                if sample_task and sample_task.solution_text_svg:
                    self.stdout.write(f"Sample task {sample_task.id}: solution_text_svg length = {len(sample_task.solution_text_svg)}")
                else:
                    self.stdout.write(self.style.WARNING(f"Sample task check failed: solution_text_svg is NULL"))

        # Финальная проверка базы данных
        self.stdout.write("Final database check for tasks 1–20...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, LENGTH(solution_text_svg) FROM tasks_task WHERE id <= 20")
            results = cursor.fetchall()
            for task_id, svg_length in results:
                self.stdout.write(f"Task {task_id}: solution_text_svg length = {svg_length if svg_length else 'NULL'}")

        self.stdout.write(self.style.SUCCESS(f"Import completed: {processed_tasks} tasks processed, {skipped_tasks} tasks skipped"))
        if failed_tasks:
            self.stdout.write(self.style.WARNING(f"Failed tasks: {failed_tasks}"))