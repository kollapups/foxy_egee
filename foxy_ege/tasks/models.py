from django.db import models
from PIL import Image, ImageDraw, ImageFont
import io
from django.core.files.base import ContentFile
import os
from enum import Enum
from django.contrib.auth.models import User
from django.conf import settings
import re
from django.utils.safestring import mark_safe


class PageVisit(models.Model):
    url = models.CharField(max_length=255, verbose_name="URL страницы")
    visit_count = models.PositiveIntegerField(default=0, verbose_name="Количество посещений")
    last_visited = models.DateTimeField(auto_now=True, verbose_name="Последнее посещение")
    is_bot = models.BooleanField(default=False, verbose_name="Бот")

    class Meta:
        verbose_name = "Посещение страницы"
        verbose_name_plural = "Посещения страниц"
        indexes = [
            models.Index(fields=['url']),
        ]

    def __str__(self):
        return f"{self.url} - {self.visit_count} посещений"

class ExamSubject(Enum):
    MATH = "math"
    MATHB = "mathb"
    PHYS = "phys"
    CHEM = "chem"
    BIO = "bio"
    HIST = "hist"
    SOC = "soc"
    LIT = "lit"
    GEO = "geo"
    ENG = "eng"
    INF = "inf"
    RUS = "rus"


class ExamPart(models.Model):
    subject = models.CharField(
        max_length=10,
        choices=[(s.value, s.name) for s in ExamSubject],
        default=ExamSubject.MATH.value,
        verbose_name="Предмет",
    )
    name = models.CharField(max_length=50, verbose_name="Название части экзамена")
    description = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Описание"
    )

    def __str__(self):
        return f"{self.name} ({self.get_subject_display()})"


class ExamLine(models.Model):
    subject = models.CharField(
        max_length=10,
        choices=[(s.value, s.name) for s in ExamSubject],
        default=ExamSubject.MATH.value,
        verbose_name="Предмет",
    )
    number = models.PositiveIntegerField(verbose_name="Номер задания на экзамене")
    description = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Описание"
    )

    class Meta:
        unique_together = [("subject", "number")]

    def __str__(self):
        return f"Задание {self.number}"


class Topic(models.Model):
    subject = models.CharField(
        max_length=10,
        choices=[(s.value, s.name) for s in ExamSubject],
        default=ExamSubject.MATH.value,
        verbose_name="Предмет",
    )
    name = models.CharField(max_length=100, verbose_name="Название темы")

    def __str__(self):
        return f"{self.name} ({self.get_subject_display()})"


class Subtopic(models.Model):
    subject = models.CharField(
        max_length=10,
        choices=[(s.value, s.name) for s in ExamSubject],
        default=ExamSubject.MATH.value,
        verbose_name="Предмет",
    )
    name = models.CharField(max_length=100, verbose_name="Название подтемы")
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="subtopics", verbose_name="Тема"
    )

    def __str__(self):
        return f"{self.name} ({self.get_subject_display()})"


class Source(models.Model):
    subject = models.CharField(
        max_length=10,
        choices=[(s.value, s.name) for s in ExamSubject],
        default=ExamSubject.MATH.value,
        verbose_name="Предмет",
    )
    name = models.CharField(max_length=100, verbose_name="Название источника")

    def __str__(self):
        return f"{self.name} ({self.get_subject_display()})"


class Task(models.Model):
    subject = models.CharField(
        max_length=10,
        choices=[(s.value, s.name) for s in ExamSubject],
        default=ExamSubject.MATH.value,
        verbose_name="Предмет",
    )
    unique_id = models.CharField(
        max_length=50, unique=True, verbose_name="Уникальный номер задания"
    )
    text = models.TextField(verbose_name="Текст задания")
    text_svg = models.TextField(
        blank=True, null=True, verbose_name="Текст задания в SVG"
    )
    latex_formula = models.TextField(
        blank=True, null=True, verbose_name="LaTeX-формула"
    )
    latex_formula_svg = models.TextField(
        blank=True, null=True, verbose_name="LaTeX-формула в SVG"
    )
    formula_image = models.ImageField(
        upload_to="formula_images/",
        blank=True,
        null=True,
        verbose_name="Изображение формулы",
    )
    image = models.ImageField(
        upload_to="task_images/",
        blank=True,
        null=True,
        verbose_name="Изображение к заданию",
    )
    exam_part = models.ForeignKey(
        ExamPart, on_delete=models.SET_NULL, null=True, verbose_name="Часть экзамена"
    )
    exam_line = models.ForeignKey(
        ExamLine, on_delete=models.SET_NULL, null=True, verbose_name="Линия экзамена"
    )
    topic = models.ForeignKey(
        Topic, on_delete=models.SET_NULL, null=True, verbose_name="Тема задания"
    )
    subtopic = models.ForeignKey(
        Subtopic, on_delete=models.SET_NULL, null=True, verbose_name="Подтема задания"
    )
    source = models.ForeignKey(
        Source, on_delete=models.SET_NULL, null=True, verbose_name="Источник"
    )
    solution_text = models.TextField(
        blank=True, null=True, verbose_name="Решение (текст)"
    )
    solution_text_svg = models.TextField(
        blank=True, null=True, verbose_name="Решение в SVG"
    )
    answer = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Правильный ответ"
    )

    def has_solution(self):
        return bool(
            self.solution_text
            or self.solution_text_svg
            or self.solution_images.exists()
        )

    def __str__(self):
        return f"Задание {self.unique_id}"

    def render_to_svg(self, force=False):
        """
        Renders LaTeX formulas in text, solution_text, and latex_formula to SVG.
        Replaces [NEWLINE] and \n\n with <br> tags AFTER LaTeX rendering to ensure proper HTML rendering.
        Only updates SVG fields if they are empty or force=True.
        Note: This is a fallback for server-side rendering. Prefer local Node.js rendering.
        """
        def render_latex(latex):
            # Placeholder: Replace with actual server-side MathJax rendering if needed
            # For now, wrap LaTeX in a span with data-latex attribute to indicate it needs rendering
            # In a real implementation, this would convert LaTeX to SVG
            return f'<span class="mathjax" data-latex="{latex}">{latex}</span>'  # TODO: Implement actual SVG rendering

        # Regular expression for LaTeX delimiters
        latex_pattern = (
            r"\$\$([\s\S]*?)\$\$|\$([\s\S]*?)\$|\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)"
        )

        def process_text(text):
            if not text:
                return text

            # Сначала обрабатываем LaTeX-формулы
            result = ""
            last_index = 0
            for match in re.finditer(latex_pattern, text):
                # Добавляем текст до LaTeX
                result += text[last_index:match.start()]
                # Извлекаем LaTeX
                latex = (
                    match.group(1) or match.group(2) or match.group(3) or match.group(4)
                )
                # Рендерим LaTeX в SVG (или placeholder)
                svg = render_latex(latex)
                result += svg
                last_index = match.end()
            # Добавляем оставшийся текст
            result += text[last_index:]

            # После обработки LaTeX заменяем [NEWLINE] и \n\n на <br>
            result = result.replace("[NEWLINE]", "<br>")
            result = result.replace("\n\n", "<br>")
            result = result.replace("\n", "<br>")  # Обрабатываем одиночные \n тоже

            return result

        # Обновляем поля SVG, только если они пусты или force=True
        if force or not self.text_svg:
            self.text_svg = process_text(self.text) if self.text else None
        if force or not self.solution_text_svg:
            self.solution_text_svg = process_text(self.solution_text) if self.solution_text else None
        if force or not self.latex_formula_svg:
            self.latex_formula_svg = render_latex(self.latex_formula) if self.latex_formula else None

        # Не вызываем save() здесь, чтобы избежать рекурсии
        # Вызов save() должен быть выполнен явно, если нужно

    def save(self, *args, skip_svg_render=False, **kwargs):

        # Apply watermark to image if present
        if self.image and os.path.exists(self.image.path):
            img = Image.open(self.image.path).convert("RGBA")
            watermark = Image.new("RGBA", img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark)
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            watermark_text = "FoxyEGE.ru"
            text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            position = ((img.width - text_width) // 2, (img.height - text_height) // 2)
            draw.text(position, watermark_text, font=font, fill=(0, 0, 0, 100))
            watermarked_img = Image.alpha_composite(img, watermark)
            buffer = io.BytesIO()
            watermarked_img.convert("RGB").save(buffer, format="JPEG")
            buffer.seek(0)
            file_name = self.image.name
            self.image.delete(save=False)
            self.image.save(file_name, ContentFile(buffer.read()), save=False)
            buffer.close()

        # Skip SVG rendering if explicitly requested
        if not skip_svg_render:
            # Do NOT call render_to_svg automatically
            pass

        super().save(*args, **kwargs)


class SolutionImage(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="solution_images",
        verbose_name="Задание",
    )
    image = models.ImageField(
        upload_to="solution_images/", verbose_name="Изображение решения"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")
    width = models.PositiveIntegerField(
        default=300,
        verbose_name="Ширина изображения (px)",
        help_text="Укажите ширину изображения в пикселях (например, 300). Высота будет автоматически подстроена.",
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Изображение для задания {self.task.unique_id} (Порядок: {self.order})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and os.path.exists(self.image.path):
            img = Image.open(self.image.path).convert("RGBA")
            watermark = Image.new("RGBA", img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark)
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            watermark_text = "FoxyEGE.ru"
            text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            position = ((img.width - text_width) // 2, (img.height - text_height) // 2)
            draw.text(position, watermark_text, font=font, fill=(0, 0, 0, 100))
            watermarked_img = Image.alpha_composite(img, watermark)
            buffer = io.BytesIO()
            watermarked_img.convert("RGB").save(buffer, format="JPEG")
            buffer.seek(0)
            file_name = self.image.name
            self.image.delete(save=False)
            self.image.save(file_name, ContentFile(buffer.read()), save=False)
            buffer.close()
        super().save(*args, **kwargs)


class Comment(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="comments", verbose_name="Задание"
    )
    author = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True,
        verbose_name="Автор",
    )
    author_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Имя автора (если не авторизован)",
    )
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_approved = models.BooleanField(
        default=False, verbose_name="Одобрено модератором"
    )

    def __str__(self):
        author_display = (
            self.author.display_name if self.author else self.author_name or "Аноним"
        )
        return f"Комментарий от {author_display} к заданию {self.task.unique_id}"


class GeneratedVariant(models.Model):
    subject = models.CharField(
        max_length=10,
        choices=[(s.value, s.name) for s in ExamSubject],
        default=ExamSubject.MATH.value,
        verbose_name="Предмет",
    )
    variant_id = models.CharField(
        max_length=255, unique=True, verbose_name="Уникальный ID варианта"
    )
    tasks = models.ManyToManyField(
        Task, related_name="variants", verbose_name="Задания"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания варианта"
    )

    def __str__(self):
        return f"Variant {self.variant_id} ({self.get_subject_display()})"

    class Meta:
        verbose_name = "Сгенерированный вариант"
        verbose_name_plural = "Сгенерированные варианты"


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorite_tasks",
        verbose_name="Пользователь",
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="favorited_by",
        verbose_name="Задание",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        unique_together = ("user", "task")
        verbose_name = "Избранное задание"
        verbose_name_plural = "Избранные задания"

    def __str__(self):
        return f"{self.user.username} - {self.task.unique_id}"
