from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def split_steps(svg_content):
    """
    Разделяет solution_text_svg на шаги решения.
    - Разделение происходит по <br> тегам, которые были преобразованы из [NEWLINE] или \n\n.
    - Inline-формулы (\(...\)) и display-формулы (\[...\]) остаются в строке с текстом.
    - Каждый шаг оборачивается в <div class="solution-step"> с учетом типа содержимого.
    """
    if not svg_content:
        return []

    # Удаляем лишние пробелы
    cleaned_content = svg_content.strip()

    # Разделяем по <br>
    steps = cleaned_content.split('<br>')

    # Обрабатываем шаги
    processed_steps = []
    for step in steps:
        step = step.strip()
        if not step:
            continue
        # Проверяем, содержит ли шаг SVG и какой тип формулы
        if '<svg' in step:
            # Если это complex-формула, добавляем класс complex-step
            if 'data-latex-type="complex"' in step:
                processed_steps.append(mark_safe(f'<div class="solution-step complex-step">{step}</div>'))
            else:
                processed_steps.append(mark_safe(f'<div class="solution-step">{step}</div>'))
        else:
            # Для текста без SVG
            processed_steps.append(mark_safe(f'<div class="solution-step text-step">{step}</div>'))

    return processed_steps