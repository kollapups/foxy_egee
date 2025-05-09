from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()


@register.filter
def get_item(queryset, pk):
    """
    Возвращает объект из Queryset по заданному первичному ключу (pk).
    Если объект не найден, возвращает None.
    """
    try:
        return queryset.get(id=pk)
    except queryset.model.DoesNotExist:
        return None


@register.filter
def render_solution_text(text, solution_images):
    """
    Рендерит текст решения, заменяя плейсхолдеры [image:N] на изображения из solution_images.
    Нумерация начинается с 0, соответствует полю order в SolutionImage.
    """
    if not text or not solution_images:
        return mark_safe(text or "")
    images = list(solution_images.order_by("order"))

    def replace_image_tag(match):
        image_index = int(match.group(1))
        if 0 <= image_index < len(images):
            img = images[image_index]
            return f'<img src="{img.image.url}" alt="Решение {image_index}" style="max-width: {img.width}px; height: auto;" class="solution-image">'
        return match.group(0)

    rendered_text = re.sub(r"\[image:(\d+)\]", replace_image_tag, text)
    return mark_safe(rendered_text)


@register.filter
def querystring(request_get, **kwargs):
    """
    Создает строку запроса, сохраняя существующие параметры и добавляя новые из kwargs.
    Используется для пагинации.
    """
    query_dict = request_get.copy()
    for key, value in kwargs.items():
        query_dict[key] = value
    return query_dict.urlencode()
