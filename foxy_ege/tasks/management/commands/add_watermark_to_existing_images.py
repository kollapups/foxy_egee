from django.core.management.base import BaseCommand
from django.apps import apps
from PIL import Image, ImageDraw, ImageFont
import io
from django.core.files.base import ContentFile
import os
import logging

# Настройка логирования для отладки
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Adds watermark to existing images in task_images and solution_images"

    def handle(self, *args, **options):
        try:
            # Динамически получаем модели
            Task = apps.get_model("tasks", "Task")
            SolutionImage = apps.get_model("tasks", "SolutionImage")

            # Обработка изображений для Task
            tasks = Task.objects.all()
            for task in tasks:
                if task.image and os.path.exists(task.image.path):
                    self.add_watermark(task.image.path, task.image)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Watermark added to task image: {task.unique_id}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"No image or path does not exist for task: {task.unique_id}"
                        )
                    )

            # Обработка изображений для SolutionImage
            solution_images = SolutionImage.objects.all()
            for solution_img in solution_images:
                if solution_img.image and os.path.exists(solution_img.image.path):
                    self.add_watermark(solution_img.image.path, solution_img.image)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Watermark added to solution image: {solution_img.id}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"No image or path does not exist for solution image: {solution_img.id}"
                        )
                    )

            self.stdout.write(
                self.style.SUCCESS("Successfully added watermarks to existing images")
            )

        except Exception as e:
            logger.error(f"Error in add_watermark_to_existing_images: {str(e)}")
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))

    def add_watermark(self, image_path, image_field):
        try:
            img = Image.open(image_path).convert("RGBA")
            watermark = Image.new("RGBA", img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark)
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                logger.warning("Arial font not found, using default font")
                font = ImageFont.load_default()
            watermark_text = "FoxyEGE.ru"
            text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            position = ((img.width - text_width) // 2, (img.height - text_height) // 2)
            draw.text(position, watermark_text, font=font, fill=(0, 0, 0, 50))
            watermarked_img = Image.alpha_composite(img, watermark)
            buffer = io.BytesIO()
            watermarked_img.convert("RGB").save(buffer, format="JPEG")
            buffer.seek(0)
            file_name = image_field.name
            image_field.delete(save=False)  # Удаляем старое изображение
            image_field.save(
                file_name, ContentFile(buffer.read()), save=False
            )  # Сохраняем новое
            buffer.close()
        except Exception as e:
            logger.error(f"Error adding watermark to {image_path}: {str(e)}")
            self.stdout.write(
                self.style.ERROR(f"Error adding watermark to {image_path}: {str(e)}")
            )
