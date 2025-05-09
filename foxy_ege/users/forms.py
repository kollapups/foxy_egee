from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from tasks.models import ExamPart, ExamLine, Topic, Subtopic, Source

EXAM_MAX_TASKS = {
    "math": 19,  # Пример, настройте под свои предметы
    # Добавьте другие предметы, если нужно
}


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False, label="Email (опционально)")
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES, required=True, label="Роль"
    )
    teacher_code = forms.CharField(required=False, label="Код учителя (опционально)")

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "role", "teacher_code")

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        username = self.cleaned_data.get("username")
        if len(password1) < 8:
            raise forms.ValidationError("Пароль должен содержать минимум 8 символов.")
        if password1 == username:
            raise forms.ValidationError(
                "Пароль не должен совпадать с именем пользователя."
            )
        if password1.isdigit():
            raise forms.ValidationError("Пароль не может состоять только из цифр.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.role = self.cleaned_data["role"]
        if commit:
            user.save()
        return user


class TaskGeneratorForm(forms.Form):
    def __init__(self, subject=None, homework_type=None, *args, **kwargs):
        # Извлекаем только те kwargs, которые принимает django.forms.Form
        form_kwargs = {}
        for key in ["data", "initial", "prefix", "auto_id", "label_suffix"]:
            if key in kwargs:
                form_kwargs[key] = kwargs[key]

        # Вызываем родительский конструктор с отфильтрованными kwargs
        super().__init__(*args, **form_kwargs)

        # Сохраняем subject и homework_type как атрибуты формы
        self.subject = subject
        self.homework_type = homework_type

        # Настройка полей формы на основе subject
        if subject:
            self.fields["parts"].queryset = ExamPart.objects.filter(subject=subject)
            self.fields["exam_lines"].queryset = ExamLine.objects.filter(
                subject=subject
            )
            self.fields["topics"].queryset = Topic.objects.filter(subject=subject)
            self.fields["subtopics"].queryset = Subtopic.objects.filter(subject=subject)
            self.fields["sources"].queryset = Source.objects.filter(subject=subject)
            self.fields["task_count"].max_value = EXAM_MAX_TASKS.get(subject, 19)

        # Настройка поля task_count в зависимости от homework_type
        if homework_type == "random":
            self.fields["task_count"].required = True
        else:
            self.fields["task_count"].required = False

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
        max_value = self.fields["task_count"].max_value
        if task_count < 1 or task_count > max_value:
            raise forms.ValidationError(
                f"Количество заданий должно быть от 1 до {max_value}."
            )
        if self.homework_type == "random" and not task_count:
            raise forms.ValidationError(
                "Для случайного выбора укажите количество заданий."
            )
        return task_count
