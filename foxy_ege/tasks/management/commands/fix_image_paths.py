from django.core.management.base import BaseCommand
from tasks.models import Task, SolutionImage

class Command(BaseCommand):
    help = 'Fixes incorrect image paths in Task and SolutionImage models'

    def handle(self, *args, **kwargs):
        # Fix Task images
        task_count = 0
        for task in Task.objects.exclude(image__isnull=True):
            original_path = task.image.name
            # Remove repeated 'task_images/' segments
            if 'task_images/task_images/' in original_path:
                correct_path = original_path.replace('task_images/task_images/', 'task_images/')
                task.image.name = correct_path
                task.save()
                task_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Fixed Task {task.unique_id}: {original_path} -> {task.image.name}'
                ))

        # Fix SolutionImage images
        solution_count = 0
        for sol_img in SolutionImage.objects.all():
            original_path = sol_img.image.name
            if 'solution_images/solution_images/' in original_path:
                correct_path = original_path.replace('solution_images/solution_images/', 'solution_images/')
                sol_img.image.name = correct_path
                sol_img.save()
                solution_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Fixed SolutionImage for Task {sol_img.task.unique_id}: {original_path} -> {sol_img.image.name}'
                ))

        self.stdout.write(self.style.SUCCESS(
            f'Fixed {task_count} Task images and {solution_count} SolutionImage images.'
        ))