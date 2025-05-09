from django.core.management.base import BaseCommand
from tasks.models import Task
import re

class Command(BaseCommand):
    help = "Nullify text and solution_text for tasks with valid SVG"

    def is_valid_svg(self, content):
        if not content or not isinstance(content, str):
            return False
        return bool(re.match(r'^\s*<svg\b', content, re.IGNORECASE) and '</svg>' in content)

    def handle(self, *args, **options):
        tasks = Task.objects.all()
        processed = 0
        skipped = 0

        for task in tasks:
            try:
                text_svg_valid = self.is_valid_svg(task.text_svg)
                solution_svg_valid = self.is_valid_svg(task.solution_text_svg)

                if text_svg_valid and solution_svg_valid:
                    task.text = None
                    task.solution_text = None
                    task.save()
                    self.stdout.write(self.style.SUCCESS(f"Nullified text and solution_text for task {task.id}"))
                    processed += 1
                else:
                    self.stdout.write(self.style.WARNING(f"Skipped task {task.id}: invalid SVG"))
                    skipped += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing task {task.id}: {str(e)}"))
                skipped += 1

        self.stdout.write(self.style.SUCCESS(f"Processed {processed} tasks, skipped {skipped} tasks"))