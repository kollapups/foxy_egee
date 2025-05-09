from django import forms
from django.contrib import admin
from .models import (
    ExamPart,
    ExamLine,
    Topic,
    Subtopic,
    Task,
    Source,
    SolutionImage,
    Comment,
    GeneratedVariant,
)


class TaskAdminForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"


@admin.register(ExamPart)
class ExamPartAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "subject")
    list_filter = ("subject",)


@admin.register(ExamLine)
class ExamLineAdmin(admin.ModelAdmin):
    list_display = ("number", "description", "subject")
    list_filter = ("subject",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "subject")
    list_filter = ("subject",)


@admin.register(Subtopic)
class SubtopicAdmin(admin.ModelAdmin):
    list_display = ("name", "topic", "subject")
    list_filter = ("topic", "subject")


class SolutionImageInline(admin.TabularInline):
    model = SolutionImage
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm
    list_display = (
        "unique_id",
        "exam_part",
        "exam_line",
        "topic",
        "subtopic",
        "subject",
    )
    list_filter = ("exam_part", "exam_line", "topic", "subtopic", "subject")
    search_fields = ("unique_id", "text")
    inlines = [SolutionImageInline]

    class Media:
        js = (
            "admin/js/vendor/jquery/jquery.min.js",  # Явно подключаем jQuery
            "admin/js/task_filter.js",
        )


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("name", "subject")
    list_filter = ("subject",)


@admin.register(SolutionImage)
class SolutionImageAdmin(admin.ModelAdmin):
    list_display = ("task", "order", "width")
    list_filter = ("task__subject",)
    list_editable = ("order", "width")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author_name", "task", "created_at", "is_approved")
    list_filter = ("is_approved", "task__subject")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    approve_comments.short_description = "Одобрить выбранные комментарии"


@admin.register(GeneratedVariant)
class GeneratedVariantAdmin(admin.ModelAdmin):
    list_display = ("variant_id", "subject", "created_at")
    list_filter = ("subject",)
