from django import forms
from .models import Comment, Topic, Subtopic, ExamLine, Source, ExamPart
from .constants import EXAM_MAX_TASKS


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["author_name", "text"]
        widgets = {
            "author_name": forms.TextInput(attrs={"placeholder": "Ваше имя"}),
            "text": forms.Textarea(
                attrs={"placeholder": "Введите ваш комментарий...", "rows": 4}
            ),
        }
        labels = {
            "author_name": "Имя",
            "text": "Комментарий",
        }


class VariantGeneratorForm(forms.Form):
    def __init__(self, subject=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if subject:
            self.fields["exam_lines"].queryset = ExamLine.objects.filter(
                subject=subject
            )
            self.fields["topics"].queryset = Topic.objects.filter(subject=subject)
            self.fields["subtopics"].queryset = Subtopic.objects.filter(subject=subject)
            self.fields["sources"].queryset = Source.objects.filter(subject=subject)
            self.fields["parts"].queryset = ExamPart.objects.filter(subject=subject)

    exam_lines = forms.ModelMultipleChoiceField(
        queryset=ExamLine.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Линии экзамена",
    )
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Темы",
    )
    subtopics = forms.ModelMultipleChoiceField(
        queryset=Subtopic.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Подтемы",
    )
    sources = forms.ModelMultipleChoiceField(
        queryset=Source.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Источники",
    )
    parts = forms.ModelMultipleChoiceField(
        queryset=ExamPart.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Части экзамена",
    )

    def clean(self):
        cleaned_data = super().clean()
        if not any(
            [
                cleaned_data.get("exam_lines"),
                cleaned_data.get("topics"),
                cleaned_data.get("subtopics"),
                cleaned_data.get("sources"),
                cleaned_data.get("parts"),
            ]
        ):
            raise forms.ValidationError(
                "Выберите хотя бы один параметр для фильтрации."
            )
        return cleaned_data


class TaskGeneratorForm(forms.Form):
    def __init__(self, subject=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if subject:
            self.fields["parts"].queryset = ExamPart.objects.filter(subject=subject)
            self.fields["exam_lines"].queryset = ExamLine.objects.filter(
                subject=subject
            )
            self.fields["topics"].queryset = Topic.objects.filter(subject=subject)
            self.fields["subtopics"].queryset = Subtopic.objects.filter(subject=subject)
            self.fields["sources"].queryset = Source.objects.filter(subject=subject)
            self.fields["task_count"].max_value = EXAM_MAX_TASKS.get(subject, 19)

    parts = forms.ModelMultipleChoiceField(
        queryset=ExamPart.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Части экзамена",
    )
    exam_lines = forms.ModelMultipleChoiceField(
        queryset=ExamLine.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Задания экзамена",
    )
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Темы",
    )
    subtopics = forms.ModelMultipleChoiceField(
        queryset=Subtopic.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Подтемы",
    )
    sources = forms.ModelMultipleChoiceField(
        queryset=Source.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Источники",
    )
    task_count = forms.IntegerField(
        min_value=1,
        max_value=40,
        initial=1,
        label="Количество заданий",
        widget=forms.NumberInput(attrs={"style": "width: 100px;"}),
    )

    def clean_task_count(self):
        task_count = self.cleaned_data["task_count"]
        if task_count < 1 or task_count > self.fields["task_count"].max_value:
            raise forms.ValidationError(
                f"Количество заданий должно быть от 1 до {self.fields['task_count'].max_value}."
            )
        return task_count
