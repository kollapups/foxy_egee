from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_file_size(value):
    max_size = 5 * 1024 * 1024  # 5 МБ
    if value.size > max_size:
        raise ValidationError(
            f"Размер файла не должен превышать 5 МБ. Ваш файл: {value.size / (1024 * 1024):.2f} МБ"
        )


def validate_submission_file_size(value):
    max_size = 2 * 1024 * 1024  # 2 МБ
    if value.size > max_size:
        raise ValidationError(
            f"Размер файла не должен превышать 2 МБ. Ваш файл: {value.size / (1024 * 1024):.2f} МБ"
        )


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("student", "Ученик"),
        ("teacher", "Учитель"),
    )
    unique_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")
    display_name = models.CharField(max_length=100, blank=True, null=True)
    teacher_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    specialty = models.CharField(max_length=255, blank=True, null=True)
    teachers = models.ManyToManyField(
        "self", through="StudentTeacher", symmetrical=False, related_name="students"
    )
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="users_customuser_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="users_customuser_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = str(uuid.uuid4())[:10]
        if self.role == "teacher" and not self.teacher_code:
            self.teacher_code = str(uuid.uuid4())[:10]
        if not self.display_name:
            self.display_name = self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return self.display_name or self.username


class StudentTeacher(models.Model):
    student = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="student_teachers"
    )
    teacher = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="teacher_students"
    )

    class Meta:
        unique_together = ("student", "teacher")

    def __str__(self):
        return f"{self.student} -> {self.teacher}"


class Homework(models.Model):
    HOMEWORK_TYPE_CHOICES = (
        ("upload", "Загрузка файлов"),
        ("manual", "Выбор вручную"),
        ("random", "Случайный выбор"),
    )
    teacher = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="assigned_homeworks"
    )
    students = models.ManyToManyField(CustomUser, related_name="received_homeworks")
    tasks = models.ManyToManyField("tasks.Task", blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    homework_type = models.CharField(max_length=10, choices=HOMEWORK_TYPE_CHOICES)
    uploaded_files = models.FileField(
        upload_to="homework_files/",
        null=True,
        blank=True,
        validators=[validate_file_size],
    )
    answers = models.JSONField(null=True, blank=True)
    image_size = models.CharField(max_length=10, default="150")

    def __str__(self):
        return f"{self.title} ({self.teacher.display_name})"


class HomeworkFile(models.Model):
    homework = models.ForeignKey(
        Homework, on_delete=models.CASCADE, related_name="files"
    )
    file = models.FileField(upload_to="homework_files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.homework.title} - {self.file.name}"


class StudentHomework(models.Model):
    STATUS_CHOICES = (
        ("pending", "Ожидает выполнения"),
        ("in_progress", "В процессе"),
        ("completed", "Завершено"),
    )
    student = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="student_homeworks"
    )
    homework = models.ForeignKey(
        Homework, on_delete=models.CASCADE, related_name="student_submissions"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    student_answers = models.JSONField(null=True, blank=True)
    results = models.JSONField(null=True, blank=True)
    submission_file = models.FileField(
        upload_to="student_submissions/",
        null=True,
        blank=True,
        validators=[validate_submission_file_size],
    )

    def save(self, *args, **kwargs):
        if self.status == "in_progress" and not self.start_time:
            self.start_time = timezone.now()
        if self.status == "completed" and not self.end_time:
            self.end_time = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.display_name} - {self.homework.title}"
