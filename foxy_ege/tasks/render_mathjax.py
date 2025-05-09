import subprocess
import os
import re
import cairosvg
import uuid
from django.conf import settings


def render_mathjax(latex, output_dir=os.path.join(settings.STATIC_ROOT, "formulas")):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Путь к render_mathjax.js относительно проекта
    render_js_path = os.path.join(settings.BASE_DIR, "render_mathjax.js")

    try:
        # Проверяем, существует ли файл
        if not os.path.exists(render_js_path):
            raise FileNotFoundError(f"Файл {render_js_path} не найден")

        # Вызываем Node.js для рендеринга LaTeX в CHTML
        result = subprocess.run(
            ["node", render_js_path, latex],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=10,
        )

        if result.returncode != 0:
            print(f"Ошибка в Node.js: {result.stderr}")
            return f'<span style="color: red;">Ошибка рендеринга: {latex}</span>'

        chtml_content = result.stdout.strip()

        # Генерируем уникальное имя файла
        filename = f"formula_{uuid.uuid4().hex}.png"
        output_path = os.path.join(output_dir, filename)

        # Конвертируем CHTML в PNG через временный SVG (cairosvg не работает напрямую с CHTML, поэтому нужен промежуточный шаг)
        temp_svg_path = os.path.join(output_dir, f"temp_{uuid.uuid4().hex}.svg")
        with open(temp_svg_path, "w", encoding="utf-8") as f:
            f.write(f"<svg><foreignObject>{chtml_content}</foreignObject></svg>")
        cairosvg.svg2png(file_obj=open(temp_svg_path, "rb"), write_to=output_path)
        os.remove(temp_svg_path)

        # Возвращаем путь относительно статики
        return f"/static/formulas/{filename}"

    except subprocess.TimeoutExpired:
        print(f"Таймаут при рендеринге формулы: {latex}")
        return f'<span style="color: red;">Таймаут рендеринга: {latex}</span>'
    except FileNotFoundError as e:
        print(f"Ошибка: {str(e)}")
        return (
            f'<span style="color: red;">Ошибка: файл render_mathjax.js не найден</span>'
        )
    except Exception as e:
        print(f"Ошибка при рендеринге формулы: {latex}, ошибка: {str(e)}")
        return f'<span style="color: red;">Ошибка: {latex}</span>'


def process_latex_in_text(text):
    if not text:
        return text

    # Ищем формулы в тексте
    inline_pattern = r"(?<!\\)\$(.*?)(?<!\\)\$"
    display_pattern = r"\$\$(.*?)\$\$"

    def replace_inline(match):
        latex = match.group(1)
        if latex:
            img_path = render_mathjax(latex)
            return (
                f'<img src="{img_path}" alt="Formula" style="vertical-align: middle;">'
            )
        return match.group(0)

    def replace_display(match):
        latex = match.group(1)
        if latex:
            img_path = render_mathjax(latex)
            return f'<div style="text-align: center;"><img src="{img_path}" alt="Formula"></div>'
        return match.group(0)

    # Заменяем формулы на изображения
    text = re.sub(inline_pattern, replace_inline, text)
    text = re.sub(display_pattern, replace_display, text)
    return text
