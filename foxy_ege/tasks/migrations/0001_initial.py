# Generated by Django 5.1.7 on 2025-04-04 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя автора (если не авторизован)')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_approved', models.BooleanField(default=False, verbose_name='Одобрено модератором')),
            ],
        ),
        migrations.CreateModel(
            name='ExamLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(choices=[('math', 'MATH'), ('mathb', 'MATHB'), ('phys', 'PHYS'), ('chem', 'CHEM'), ('bio', 'BIO'), ('hist', 'HIST'), ('soc', 'SOC'), ('lit', 'LIT'), ('geo', 'GEO'), ('eng', 'ENG'), ('inf', 'INF'), ('rus', 'RUS')], default='math', max_length=10, verbose_name='Предмет')),
                ('number', models.PositiveIntegerField(verbose_name='Номер задания на экзамене')),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='ExamPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(choices=[('math', 'MATH'), ('mathb', 'MATHB'), ('phys', 'PHYS'), ('chem', 'CHEM'), ('bio', 'BIO'), ('hist', 'HIST'), ('soc', 'SOC'), ('lit', 'LIT'), ('geo', 'GEO'), ('eng', 'ENG'), ('inf', 'INF'), ('rus', 'RUS')], default='math', max_length=10, verbose_name='Предмет')),
                ('name', models.CharField(max_length=50, verbose_name='Название части экзамена')),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
            ],
            options={
                'verbose_name': 'Избранное задание',
                'verbose_name_plural': 'Избранные задания',
            },
        ),
        migrations.CreateModel(
            name='GeneratedVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(choices=[('math', 'MATH'), ('mathb', 'MATHB'), ('phys', 'PHYS'), ('chem', 'CHEM'), ('bio', 'BIO'), ('hist', 'HIST'), ('soc', 'SOC'), ('lit', 'LIT'), ('geo', 'GEO'), ('eng', 'ENG'), ('inf', 'INF'), ('rus', 'RUS')], default='math', max_length=10, verbose_name='Предмет')),
                ('variant_id', models.CharField(max_length=255, unique=True, verbose_name='Уникальный ID варианта')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания варианта')),
            ],
            options={
                'verbose_name': 'Сгенерированный вариант',
                'verbose_name_plural': 'Сгенерированные варианты',
            },
        ),
        migrations.CreateModel(
            name='SolutionImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='solution_images/', verbose_name='Изображение решения')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')),
                ('width', models.PositiveIntegerField(default=300, help_text='Укажите ширину изображения в пикселях (например, 300). Высота будет автоматически подстроена.', verbose_name='Ширина изображения (px)')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(choices=[('math', 'MATH'), ('mathb', 'MATHB'), ('phys', 'PHYS'), ('chem', 'CHEM'), ('bio', 'BIO'), ('hist', 'HIST'), ('soc', 'SOC'), ('lit', 'LIT'), ('geo', 'GEO'), ('eng', 'ENG'), ('inf', 'INF'), ('rus', 'RUS')], default='math', max_length=10, verbose_name='Предмет')),
                ('name', models.CharField(max_length=100, verbose_name='Название источника')),
            ],
        ),
        migrations.CreateModel(
            name='Subtopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(choices=[('math', 'MATH'), ('mathb', 'MATHB'), ('phys', 'PHYS'), ('chem', 'CHEM'), ('bio', 'BIO'), ('hist', 'HIST'), ('soc', 'SOC'), ('lit', 'LIT'), ('geo', 'GEO'), ('eng', 'ENG'), ('inf', 'INF'), ('rus', 'RUS')], default='math', max_length=10, verbose_name='Предмет')),
                ('name', models.CharField(max_length=100, verbose_name='Название подтемы')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(choices=[('math', 'MATH'), ('mathb', 'MATHB'), ('phys', 'PHYS'), ('chem', 'CHEM'), ('bio', 'BIO'), ('hist', 'HIST'), ('soc', 'SOC'), ('lit', 'LIT'), ('geo', 'GEO'), ('eng', 'ENG'), ('inf', 'INF'), ('rus', 'RUS')], default='math', max_length=10, verbose_name='Предмет')),
                ('unique_id', models.CharField(max_length=50, unique=True, verbose_name='Уникальный номер задания')),
                ('text', models.TextField(verbose_name='Текст задания')),
                ('latex_formula', models.TextField(blank=True, null=True, verbose_name='LaTeX-формула')),
                ('image', models.ImageField(blank=True, null=True, upload_to='task_images/', verbose_name='Изображение к заданию')),
                ('solution_text', models.TextField(blank=True, null=True, verbose_name='Решение (текст)')),
                ('answer', models.CharField(blank=True, max_length=255, null=True, verbose_name='Правильный ответ')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(choices=[('math', 'MATH'), ('mathb', 'MATHB'), ('phys', 'PHYS'), ('chem', 'CHEM'), ('bio', 'BIO'), ('hist', 'HIST'), ('soc', 'SOC'), ('lit', 'LIT'), ('geo', 'GEO'), ('eng', 'ENG'), ('inf', 'INF'), ('rus', 'RUS')], default='math', max_length=10, verbose_name='Предмет')),
                ('name', models.CharField(max_length=100, verbose_name='Название темы')),
            ],
        ),
    ]
