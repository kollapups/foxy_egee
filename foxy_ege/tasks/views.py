
import random
import uuid
import asyncio
import logging
import os
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from playwright.async_api import async_playwright
from .models import (
    Task, ExamPart, Topic, Subtopic, ExamLine, Source, Comment,
    GeneratedVariant, SolutionImage, ExamSubject, Favorite
)
from .forms import CommentForm, VariantGeneratorForm, TaskGeneratorForm
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from svglib.svglib import svg2rlg
from io import BytesIO
from reportlab.graphics import renderPDF  # Импорт renderPDF
from reportlab.lib.utils import ImageReader  # Импорт ImageReader
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
import os
import re
from tasks.models import PageVisit

# Регистрация шрифта Times New Roman
font_path = os.path.join(os.path.dirname(__file__), 'static', 'fonts', 'dejavu-fonts-ttf', 'ttf', 'DejaVuSerif.ttf')
if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont('DejaVuSerif', font_path))
else:
    logging.error("DejaVu Serif font not found at %s", font_path)
    print("Warning: DejaVu Serif font not found, falling back to default.")

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Размеры изображений для PDF
SMALL_IMAGES = [1, 3]  # 200px
MEDIUM_IMAGES = [2, 11]  # 300px
LARGE_IMAGE = [8]  # 400px

# def accept_cookies(request):
#     if request.method == 'POST':
#         referer = request.META.get('HTTP_REFERER', '/')
#         print(f"Перенаправление на: {referer}")  # Отладочный вывод
#         response = redirect(referer)
#         response.set_cookie('cookieconsent_analytics', 'accept', max_age=31536000)
#         messages.success(request, "Cookie для аналитики успешно приняты.")
#         return response
#     return HttpResponse(status=405)

# def decline_cookies(request):
#     if request.method == 'POST':
#         response = redirect(request.META.get('HTTP_REFERER', '/'))
#         response.set_cookie('cookieconsent_analytics', 'decline', max_age=31536000)  # 1 год
#         messages.success(request, "Вы отказались от использования cookie для аналитики.")
#         return response
#     return HttpResponse(status=405)

# def delete_cookies(request):
#     response = redirect(request.META.get('HTTP_REFERER', '/'))
#     response.delete_cookie('cookieconsent_analytics')
#     messages.success(request, "Cookie для аналитики удалены.")
#     return response

# def visit_statistics(request, subject="math"):
#     if not validate_subject(subject):
#         subject = "math"
    
#     # Получаем статистику (исключаем ботов)
#     stats = PageVisit.objects.filter(is_bot=False).order_by('-visit_count')
    
#     # Общее количество посещений
#     total_visits = sum(stat.visit_count for stat in stats)
    
#     context = {
#         "subject": subject,
#         "stats": stats,
#         "total_visits": total_visits,
#     }
#     return render(request, "tasks/visit_statistics.html", context)

def get_pdf_options(format_type):
    """Возвращает настройки PDF на основе формата."""
    options = {
        "format": "A4",
        "print_background": True,
        "scale": 1,
    }
    if format_type == "landscape":
        options["landscape"] = True
    elif format_type in ["large_font", "large_margin"]:
        options["margin"] = {"top": "15mm", "bottom": "15mm", "left": "20mm", "right": "20mm"}
        if format_type == "large_margin":
            options["margin"] = {"top": "25mm", "bottom": "25mm", "left": "20mm", "right": "20mm"}
    return options

async def render_pdf_with_playwright(html_content, options, base_url):
    """Рендерит HTML в PDF с помощью Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(base_url, wait_until="networkidle")
        await page.set_content(html_content)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)
        await page.evaluate(
            """
            () => {
                const images = document.querySelectorAll('img');
                return Promise.all(
                    Array.from(images).map(img => {
                        if (img.complete) return Promise.resolve();
                        return new Promise(resolve => {
                            img.addEventListener('load', resolve);
                            img.addEventListener('error', resolve);
                        });
                    })
                );
            }
            """
        )
        pdf_buffer = await page.pdf(**options)
        await browser.close()
        return pdf_buffer

def process_task_for_pdf(task, request, with_solutions, with_answers):
    """Обрабатывает задачу для PDF, включая замену [image:N]."""
    task_data = {
        "exam_line": task.exam_line,
        "text": task.text,
        "image": task.image,
        "has_solution": task.has_solution(),
        "solution_text": task.solution_text if with_solutions and task.has_solution() else None,
        "answer": task.answer if with_answers else None,
    }
    if task_data["solution_text"]:
        solution_images = SolutionImage.objects.filter(task=task).order_by("order")
        logger.debug(f"Found solution images for task {task.unique_id}: {solution_images.count()}")
        solution_text = task_data["solution_text"]
        for img in solution_images:
            placeholder = f"[image:{img.order}]"
            if placeholder in solution_text:
                img_url = f"{request.scheme}://{request.get_host()}{img.image.url}"
                logger.debug(f"Formed image URL: {img_url}")
                img_tag = f'<img src="{img_url}" alt="Solution image {img.order}" class="solution-image" style="max-width: {img.width}px; height: auto; margin: 5mm 0; display: block;">' if os.path.exists(img.image.path) else f'<span style="color: red;">Image {img.order} not found</span>'
                solution_text = solution_text.replace(placeholder, img_tag)
                logger.debug(f"Replaced {placeholder} with: {img_tag}")
        task_data["solution_text"] = solution_text
    return task_data

def validate_subject(subject):
    """Проверяет, что предмет валиден."""
    if subject not in [s.value for s in ExamSubject]:
        logger.error(f"Invalid subject: {subject}")
        return False
    return True

def apply_task_filters(queryset, request_params):
    """Применяет фильтры к queryset задач."""
    q_conditions = Q()
    if request_params.get("exam_part"):
        q_conditions &= Q(exam_part_id=request_params["exam_part"])
    if request_params.get("topic"):
        q_conditions &= Q(topic_id=request_params["topic"])
    if request_params.get("subtopic"):
        q_conditions &= Q(subtopic_id=request_params["subtopic"])
    if request_params.get("exam_line"):
        q_conditions &= Q(exam_line_id=request_params["exam_line"])
    if request_params.get("source"):
        q_conditions &= Q(source_id=request_params["source"])
    if request_params.get("search_text"):
        q_conditions &= Q(text__icontains=request_params["search_text"])
    return queryset.filter(q_conditions) if q_conditions else queryset

def get_favorite_task_ids(request, subject):
    """Возвращает ID избранных задач для пользователя."""
    if not request.user.is_authenticated:
        return set()
    return set(
        Favorite.objects.filter(user=request.user, task__subject=subject)
        .values_list("task__unique_id", flat=True)
    )

def home(request, subject="math"):
    """Главная страница."""
    if not validate_subject(subject):
        subject = "math"
    return render(request, "tasks/home.html", {"subject": subject})

def task_list(request, subject):
    """Список задач с фильтрацией и пагинацией."""
    if not validate_subject(subject):
        return HttpResponse("Неверный предмет", status=404)

    tasks = Task.objects.filter(subject=subject).select_related("exam_part", "exam_line", "topic", "subtopic", "source")
    tasks = apply_task_filters(tasks, request.GET)

    per_page = request.GET.get("per_page", 20)
    paginator = Paginator(tasks, per_page)
    page = request.GET.get("page")
    try:
        tasks_page = paginator.page(page)
    except PageNotAnInteger:
        tasks_page = paginator.page(1)
    except EmptyPage:
        tasks_page = paginator.page(paginator.num_pages)

    context = {
        "subject": subject,
        "tasks": tasks_page,
        "exam_parts": ExamPart.objects.filter(subject=subject),
        "topics": Topic.objects.filter(subject=subject),
        "subtopics": Subtopic.objects.filter(subject=subject),
        "exam_lines": ExamLine.objects.filter(subject=subject),
        "sources": Source.objects.filter(subject=subject),
        "per_page": per_page,
        "favorite_task_ids": get_favorite_task_ids(request, subject),
    }
    return render(request, "tasks/task_list.html", context)

def task_detail(request, subject, unique_id):
    """Детальная страница задачи."""
    if not validate_subject(subject):
        return HttpResponse("Неверный предмет", status=404)

    task = get_object_or_404(Task, unique_id=unique_id, subject=subject)
    if request.method == "POST":
        if not request.user.is_authenticated:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success": False, "error": "Требуется авторизация"}, status=403)
            return redirect("users:login")
        
        text = request.POST.get("text")
        if text:
            Comment.objects.create(
                task=task,
                author=request.user,
                author_name=request.user.display_name or request.user.username,
                text=text,
                is_approved=False
            )
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success": True, "message": "Комментарий отправлен на модерацию"})
            return redirect("tasks:task_detail", subject=subject, unique_id=task.unique_id)
        else:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success": False, "error": "Текст комментария обязателен"}, status=400)

    context = {
        "subject": subject,
        "task": task,
        "approved_comments": task.comments.filter(is_approved=True),
        "favorite_task_ids": get_favorite_task_ids(request, subject),
        "is_favorite": task.unique_id in get_favorite_task_ids(request, subject),
    }
    return render(request, "tasks/task_detail.html", context)

def generate_variant(request, subject):
    """Генерация варианта экзамена."""
    if not validate_subject(subject):
        return HttpResponse("Неверный предмет", status=404)

    form = VariantGeneratorForm(subject=subject, data=request.GET or None)
    variant = []
    variant_id = str(uuid.uuid4())
    error_message = None

    if request.GET and form.is_valid():
        filters = {
            "exam_lines": form.cleaned_data.get("exam_lines", ExamLine.objects.filter(subject=subject)),
            "topics": form.cleaned_data.get("topics", Topic.objects.filter(subject=subject)),
            "subtopics": form.cleaned_data.get("subtopics", Subtopic.objects.filter(subject=subject)),
            "sources": form.cleaned_data.get("sources", Source.objects.filter(subject=subject)),
            "parts": form.cleaned_data.get("parts", ExamPart.objects.filter(subject=subject)),
        }

        tasks = Task.objects.filter(subject=subject).select_related("exam_line")
        q_conditions = Q()
        for key, values in filters.items():
            if values:
                q_conditions |= Q(**{f"{key.rstrip('s')}__in": values})
        tasks = tasks.filter(q_conditions) if q_conditions else tasks

        available_tasks = list(tasks)
        if not available_tasks:
            error_message = "Нет заданий, соответствующих выбранным фильтрам."
        else:
            unique_lines = set()
            for task in available_tasks:
                if task.exam_line.number not in unique_lines:
                    variant.append(task)
                    unique_lines.add(task.exam_line.number)
                    if len(unique_lines) >= 19:
                        break
            if not variant:
                error_message = "Недостаточно уникальных заданий для генерации варианта."
            else:
                variant.sort(key=lambda task: task.exam_line.number)
                generated_variant = GeneratedVariant.objects.create(subject=subject, variant_id=variant_id)
                generated_variant.tasks.set(variant)
    else:
        for line_number in range(1, 20):
            line = ExamLine.objects.filter(subject=subject, number=line_number).first()
            if line and Task.objects.filter(subject=subject, exam_line=line).exists():
                variant.append(random.choice(Task.objects.filter(subject=subject, exam_line=line)))
        if variant:
            variant.sort(key=lambda task: task.exam_line.number)
            generated_variant = GeneratedVariant.objects.create(subject=subject, variant_id=variant_id)
            generated_variant.tasks.set(variant)
        else:
            error_message = "Недостаточно заданий для генерации варианта."

    context = {
        "subject": subject,
        "variant": variant,
        "form": form,
        "variant_id": variant_id,
        "error_message": error_message,
        "uuid": str(uuid.uuid4()),
        "favorite_task_ids": get_favorite_task_ids(request, subject),
    }
    return render(request, "tasks/generate_variant.html", context)

def generate_variant_with_id(request, subject, variant_id):
    """Отображение сохраненного варианта."""
    if not validate_subject(subject):
        return HttpResponse("Неверный предмет", status=404)

    form = VariantGeneratorForm(subject=subject)
    try:
        generated_variant = GeneratedVariant.objects.prefetch_related("tasks").get(variant_id=variant_id, subject=subject)
        variant = list(generated_variant.tasks.all())
        variant.sort(key=lambda task: task.exam_line.number)
    except GeneratedVariant.DoesNotExist:
        return render(request, "tasks/generate_variant.html", {
            "subject": subject,
            "form": form,
            "error_message": "Сохраненный вариант не найден.",
            "uuid": str(uuid.uuid4()),
            "favorite_task_ids": get_favorite_task_ids(request, subject),
        })

    context = {
        "subject": subject,
        "variant": variant,
        "form": form,
        "variant_id": variant_id,
        "uuid": str(uuid.uuid4()),
        "favorite_task_ids": get_favorite_task_ids(request, subject),
    }
    return render(request, "tasks/generate_variant.html", context)

def generate_task(request, subject):
    """Генерация случайных задач."""
    if not validate_subject(subject):
        return HttpResponse("Неверный предмет", status=404)

    form = TaskGeneratorForm(subject=subject, data=request.GET or None)
    tasks = []
    error_message = None

    if request.GET and form.is_valid():
        task_count = form.cleaned_data.get("task_count")
        filters = {
            "parts": form.cleaned_data.get("parts", []),
            "exam_lines": form.cleaned_data.get("exam_lines", []),
            "topics": form.cleaned_data.get("topics", []),
            "subtopics": form.cleaned_data.get("subtopics", []),
            "sources": form.cleaned_data.get("sources", []),
        }
        search_text = request.GET.get("search_text")

        task_queryset = Task.objects.filter(subject=subject).select_related("exam_part", "exam_line", "topic", "subtopic", "source")
        q_conditions = Q()
        for key, values in filters.items():
            if values:
                q_conditions &= Q(**{f"{key.rstrip('s')}__in": values})
        if search_text:
            q_conditions &= Q(text__icontains=search_text)
        task_queryset = task_queryset.filter(q_conditions) if q_conditions else task_queryset

        if task_queryset.exists():
            available_tasks = list(task_queryset)
            tasks = random.sample(available_tasks, min(task_count, len(available_tasks)))
            request.session["tasks"] = [task.id for task in tasks]
        else:
            error_message = "Нет заданий, соответствующих выбранным фильтрам."

    context = {
        "subject": subject,
        "form": form,
        "tasks": tasks,
        "error_message": error_message,
        "favorite_task_ids": get_favorite_task_ids(request, subject),
    }
    return render(request, "tasks/generate_task.html", context)

def print_settings(request, subject):
    exam_part = request.GET.get('exam_part')
    exam_line = request.GET.get('exam_line')
    topic = request.GET.get('topic')
    subtopic = request.GET.get('subtopic')
    source = request.GET.get('source')
    search_text = request.GET.get('search_text')
    per_page = request.GET.get('per_page', 20)

    tasks = Task.objects.filter(subject=subject)
    if exam_part:
        tasks = tasks.filter(exam_part_id=exam_part)
    if exam_line:
        tasks = tasks.filter(exam_line_id=exam_line)
    if topic:
        tasks = tasks.filter(topic_id=topic)
    if subtopic:
        tasks = tasks.filter(subtopic_id=subtopic)
    if source:
        tasks = tasks.filter(source_id=source)
    if search_text:
        tasks = tasks.filter(text__icontains=search_text)
    tasks = tasks[:int(per_page)]

    origin_params = request.GET.dict()

    return render(request, 'tasks/print_settings.html', {
        'subject': subject,
        'tasks': tasks,
        'uuid': str(uuid.uuid4()),
        'origin_params': origin_params,
    })

def print_settings_cart(request, subject):
    task_ids = request.GET.getlist('task_ids')
    tasks = Task.objects.filter(subject=subject, unique_id__in=task_ids)
    origin_params = {'task_ids': task_ids}
    return render(request, 'tasks/print_settings.html', {
        'subject': subject,
        'tasks': tasks,
        'uuid': str(uuid.uuid4()),
        'origin_params': origin_params,
    })

def print_variants_settings(request, subject, uuid):
    """Настройки печати вариантов."""
    if not validate_subject(subject):
        return HttpResponse("Неверный предмет", status=404)
    return render(request, "tasks/print_variants_settings.html", {
        "subject": subject,
        "origin_params": {k: v for k, v in request.GET.items()},
        "uuid": uuid,
        "variant_id": request.GET.get("variant_id"),
    })

def print_settings_gentask(request, subject):
    """Настройки печати сгенерированных задач."""
    if not validate_subject(subject):
        return HttpResponse("Неверный предмет", status=404)
    task_ids = request.GET.getlist("task_ids")
    if not task_ids:
        return HttpResponse("Не выбраны задания для печати", status=400)
    return render(request, "tasks/print_settings_gentask.html", {
        "subject": subject,
        "uuid": str(uuid.uuid4()),
        "task_ids": task_ids,
    })

def is_valid_svg(content):
    """Check if the content is a valid SVG string."""
    if not content or not isinstance(content, str):
        return False
    return bool(re.match(r'^\s*<svg\b', content, re.IGNORECASE) and '</svg>' in content)

def wrap_text(text, font_name, font_size, max_width):
    """Wrap text to fit within max_width, returning a list of lines."""
    if not text:
        return []
    words = text.split()
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        word_width = stringWidth(word, font_name, font_size)
        space_width = stringWidth(" ", font_name, font_size)
        if current_width + word_width + (space_width if current_line else 0) <= max_width:
            current_line.append(word)
            current_width += word_width + (space_width if current_line else 0)
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_width = word_width

    if current_line:
        lines.append(" ".join(current_line))
    return lines

def split_text_and_svg(content):
    """Split content into a list of fragments (text or SVG) in order."""
    if not content:
        return []
    svg_regex = r'(<svg\b[^>]*>[\s\S]*?</svg>)'
    fragments = re.split(svg_regex, content)
    result = []
    for fragment in fragments:
        if re.match(r'^\s*<svg\b', fragment, re.IGNORECASE):
            result.append(('svg', fragment))
        else:
            text_parts = fragment.split('<br>')
            for part in text_parts:
                if part.strip():
                    result.append(('text', part.strip()))
    return result

def render_fragments(c, fragments, left_margin, right_margin, usable_width, page_size, y_position, font_name, font_size, top_margin, bottom_margin):
    """Render text and SVG fragments inline, managing x_position and y_position."""
    x_position = left_margin
    max_y_decrement = 7 * mm  # Default line height

    for frag_type, content in fragments:
        if frag_type == 'text':
            lines = wrap_text(content, font_name, font_size, usable_width - (x_position - left_margin))
            for line in lines:
                line_width = stringWidth(line, font_name, font_size)
                if x_position + line_width > page_size[0] - right_margin:
                    y_position -= max_y_decrement
                    if y_position < bottom_margin:
                        c.showPage()
                        y_position = top_margin
                        c.setFont(font_name, font_size)
                    x_position = left_margin
                c.drawString(x_position, y_position, line)
                x_position += line_width + stringWidth(" ", font_name, font_size)

        elif frag_type == 'svg' and is_valid_svg(content):
            try:
                svg_io = BytesIO(content.encode('utf-8'))
                drawing = svg2rlg(svg_io)
                if drawing:
                    scale = min(usable_width / drawing.width, 0.5)
                    drawing.scale(scale, scale)
                    drawing_width = drawing.width * scale
                    drawing_height = drawing.height * scale

                    # Log SVG height for debugging
                    logger.debug(f"SVG height: {drawing_height}mm (scale: {scale})")

                    # Update max_y_decrement if SVG is taller than text
                    max_y_decrement = max(max_y_decrement, drawing_height + 2 * mm)

                    # Adjust SVG position to align with text baseline
                    # Lower the SVG slightly to match the text baseline
                    svg_y_offset = -1 * mm  # Negative to lower the SVG
                    svg_y_position = y_position + svg_y_offset

                    if x_position + drawing_width > page_size[0] - right_margin:
                        y_position -= max_y_decrement
                        if y_position < bottom_margin:
                            c.showPage()
                            y_position = top_margin
                            c.setFont(font_name, font_size)
                        x_position = left_margin
                        svg_y_position = y_position + svg_y_offset

                    renderPDF.draw(drawing, c, x_position, svg_y_position)
                    x_position += drawing_width + 5
            except Exception as e:
                logger.error(f"Error rendering SVG: {str(e)}")
        else:
            logger.warning(f"Invalid SVG fragment: {content[:50]}...")

    # Return the updated y_position after rendering all fragments
    if x_position > left_margin:  # If we rendered something on the line, move to the next line
        y_position -= max_y_decrement
    return y_position

def pdf_tasks(request, subject, uuid):
    try:
        # Get parameters from GET request
        format_type = request.GET.get('format', 'portrait')
        with_answers = request.GET.get('with_answers') == '1'
        with_solutions = request.GET.get('with_solutions') == '1'

        # Fetch tasks
        try:
            tasks = Task.objects.filter(subject=subject).select_related('exam_line')
            if 'task_ids' in request.GET:
                task_ids = request.GET.getlist('task_ids')
                tasks = tasks.filter(unique_id__in=task_ids)
            else:
                if 'exam_part' in request.GET:
                    tasks = tasks.filter(exam_part_id=request.GET['exam_part'])
                if 'exam_line' in request.GET:
                    tasks = tasks.filter(exam_line_id=request.GET['exam_line'])
                if 'topic' in request.GET:
                    tasks = tasks.filter(topic_id=request.GET['topic'])
                if 'subtopic' in request.GET:
                    tasks = tasks.filter(subtopic_id=request.GET['subtopic'])
                if 'source' in request.GET:
                    tasks = tasks.filter(source_id=request.GET['source'])
                if 'search_text' in request.GET:
                    tasks = tasks.filter(text__icontains=request.GET['search_text'])
            logger.debug(f"Fetched {tasks.count()} tasks for subject {subject}")
        except Exception as e:
            logger.error(f"Error fetching tasks: {str(e)}")
            return HttpResponse("Error fetching tasks", status=500)

        # Setup PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="tasks_{uuid}.pdf"'

        # Page settings
        page_size = landscape(A4) if format_type == 'landscape' else A4
        c = canvas.Canvas(response, pagesize=page_size)

        # Margins
        left_margin = 20 * mm
        right_margin = 20 * mm
        top_margin = page_size[1] - 20 * mm
        bottom_margin = 20 * mm
        usable_width = page_size[0] - left_margin - right_margin

        # Register font
        font_path = os.path.join(os.path.dirname(__file__), 'static', 'fonts', 'dejavu-fonts-ttf', 'ttf', 'DejaVuSerif.ttf')
        try:
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('DejaVuSerif', font_path))
            else:
                logger.error(f"Font not found at {font_path}, falling back to Helvetica")
                c.setFont('Helvetica', 12)
            c.setFont('DejaVuSerif', 12)
        except Exception as e:
            logger.error(f"Error registering font: {str(e)}, falling back to Helvetica")
            c.setFont('Helvetica', 12)

        y_position = top_margin
        font_size = 12
        font_name = 'DejaVuSerif'

        for idx, task in enumerate(tasks, 1):
            logger.debug(f"Processing task {task.unique_id}")

            # Task header
            try:
                c.setFillColor(colors.HexColor("#ff6f61"))
                c.setFont(font_name, 14)
                c.drawString(left_margin, y_position, f"{idx}. Задание {task.exam_line.number}.")
                y_position -= 10 * mm
                c.setFillColor(colors.black)
                c.setFont(font_name, font_size)
            except Exception as e:
                logger.error(f"Error rendering task header for task {task.unique_id}: {str(e)}")
                continue

            # Task text (text_svg)
            if task.text_svg:
                logger.debug(f"Processing text_svg for task {task.unique_id}")
                try:
                    fragments = split_text_and_svg(task.text_svg)
                    y_position = render_fragments(c, fragments, left_margin, right_margin, usable_width, page_size, y_position, font_name, font_size, top_margin, bottom_margin)
                except Exception as e:
                    logger.error(f"Error processing text_svg for task {task.unique_id}: {str(e)}")

            else:
                logger.warning(f"No text_svg for task {task.unique_id}, skipping text")

            # Latex formula (latex_formula_svg)
            if task.latex_formula_svg and is_valid_svg(task.latex_formula_svg):
                logger.debug(f"Rendering latex_formula_svg for task {task.unique_id}")
                try:
                    svg_io = BytesIO(task.latex_formula_svg.encode('utf-8'))
                    drawing = svg2rlg(svg_io)
                    if drawing:
                        scale = min(usable_width / drawing.width, 0.5)
                        drawing.scale(scale, scale)
                        drawing_height = drawing.height * scale
                        # Log SVG height for debugging
                        logger.debug(f"latex_formula_svg height: {drawing_height}mm (scale: {scale})")
                        # Align with text baseline
                        svg_y_offset = -1 * mm  # Same offset as inline SVGs
                        svg_y_position = y_position + svg_y_offset
                        if y_position - drawing_height < bottom_margin:
                            c.showPage()
                            y_position = top_margin
                            c.setFont(font_name, font_size)
                            svg_y_position = y_position + svg_y_offset
                        renderPDF.draw(drawing, c, left_margin, svg_y_position)
                        y_position -= drawing_height + 5 * mm
                except Exception as e:
                    logger.error(f"Error rendering latex_formula_svg for task {task.unique_id}: {str(e)}")

            # Task image
            if task.image and hasattr(task.image, 'path'):
                logger.debug(f"Rendering image for task {task.unique_id}")
                try:
                    if os.path.exists(task.image.path):
                        img_reader = ImageReader(task.image.path)
                        img_width, img_height = img_reader.getSize()
                        max_width = 300 if task.exam_line.number in [2, 11] else 400 if task.exam_line.number == 8 else 100
                        scale = min(max_width / img_width, 1.0)
                        img_width *= scale
                        img_height *= scale
                        if y_position - img_height < bottom_margin:
                            c.showPage()
                            y_position = top_margin
                            c.setFont(font_name, font_size)
                        c.drawImage(task.image.path, left_margin, y_position - img_height, width=img_width, height=img_height)
                        y_position -= img_height + 5 * mm
                    else:
                        logger.warning(f"Image file not found for task {task.unique_id}: {task.image.path}")
                except Exception as e:
                    logger.error(f"Error rendering image for task {task.unique_id}: {str(e)}")

            # Solutions
            if with_solutions and task.has_solution and task.solution_text_svg:
                try:
                    c.setFont(font_name, font_size)
                    c.drawString(left_margin, y_position, "Решение:")
                    y_position -= 7 * mm
                    logger.debug(f"Processing solution_text_svg for task {task.unique_id}")

                    fragments = split_text_and_svg(task.solution_text_svg)
                    y_position = render_fragments(c, fragments, left_margin, right_margin, usable_width, page_size, y_position, font_name, font_size, top_margin, bottom_margin)

                    # Solution images
                    for solution_image in task.solution_images.all():
                        if hasattr(solution_image, 'image') and solution_image.image and os.path.exists(solution_image.image.path):
                            try:
                                img_reader = ImageReader(solution_image.image.path)
                                img_width, img_height = img_reader.getSize()
                                scale = min(300 / img_width, 1.0)
                                img_width *= scale
                                img_height *= scale
                                if y_position - img_height < bottom_margin:
                                    c.showPage()
                                    y_position = top_margin
                                    c.setFont(font_name, font_size)
                                c.drawImage(solution_image.image.path, left_margin, y_position - img_height, width=img_width, height=img_height)
                                y_position -= img_height + 5 * mm
                            except Exception as e:
                                logger.error(f"Error rendering solution image for task {task.unique_id}: {str(e)}")
                except Exception as e:
                    logger.error(f"Error processing solutions for task {task.unique_id}: {str(e)}")

            # Answers
            if with_answers and task.answer:
                try:
                    c.setFont(font_name, font_size)
                    fragments = [('text', f"Ответ: {task.answer}")]
                    y_position = render_fragments(c, fragments, left_margin, right_margin, usable_width, page_size, y_position, font_name, font_size, top_margin, bottom_margin)
                    logger.debug(f"Rendered answer for task {task.unique_id}")
                except Exception as e:
                    logger.error(f"Error rendering answer for task {task.unique_id}: {str(e)}")

            y_position -= 15 * mm
            if y_position < bottom_margin:
                c.showPage()
                y_position = top_margin
                c.setFont(font_name, font_size)

        # Footer and header
        try:
            c.setFont(font_name, 10)
            c.setFillColor(colors.grey)
            c.drawCentredString(page_size[0] / 2, 15 * mm, "© FoxyEGE.ru 2025")
            c.drawCentredString(page_size[0] / 2, page_size[1] - 10 * mm, "Сгенерировано на FoxyEGE.ru")
        except Exception as e:
            logger.error(f"Error rendering footer/header: {str(e)}")

        c.showPage()
        c.save()
        return response

    except Exception as e:
        logger.error(f"Unexpected error in pdf_tasks: {str(e)}")
        return HttpResponse("Internal server error while generating PDF", status=500)

def pdf_variant(request, subject, uuid, variant_id):
    """PDF для варианта."""
    if not validate_subject(subject):
        return HttpResponse("Неверный предмет", status=404)

    try:
        generated_variant = GeneratedVariant.objects.prefetch_related("tasks").get(variant_id=variant_id, subject=subject)
        tasks = list(generated_variant.tasks.all())
        tasks.sort(key=lambda task: task.exam_line.number)
    except GeneratedVariant.DoesNotExist:
        return HttpResponse("Вариант не найден", status=404)

    format_type = request.GET.get("format", "portrait")
    with_answers = request.GET.get("with_answers") == "1"
    with_solutions = request.GET.get("with_solutions") == "1"
    with_variant_link = request.GET.get("with_variant_link") == "1"

    processed_tasks = [process_task_for_pdf(task, request, with_solutions, with_answers) for task in tasks]
    html = render_to_string("tasks/print_variants.html", {
        "tasks": processed_tasks,
        "with_answers": with_answers,
        "with_solutions": with_solutions,
        "variant_id": variant_id,
        "format": format_type,
        "request": request,
        "with_variant_link": with_variant_link,
        "subject": subject,
    })

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="variant_{uuid}.pdf"'
    pdf_content = asyncio.run(render_pdf_with_playwright(html, get_pdf_options(format_type), f"{request.scheme}://{request.get_host()}"))
    response.write(pdf_content)
    return response

def pdf_generated_tasks(request, subject, uuid):
    """PDF для сгенерированных задач."""
    if not validate_subject(subject):
        return HttpResponse("Неверный предмет", status=404)

    form = TaskGeneratorForm(subject=subject, data=request.GET or None)
    tasks = []
    if form.is_valid():
        task_count = form.cleaned_data.get("task_count")
        filters = {
            "parts": form.cleaned_data.get("parts", []),
            "exam_lines": form.cleaned_data.get("exam_lines", []),
            "topics": form.cleaned_data.get("topics", []),
            "subtopics": form.cleaned_data.get("subtopics", []),
            "sources": form.cleaned_data.get("sources", []),
        }
        task_queryset = Task.objects.filter(subject=subject).select_related("exam_part", "exam_line", "topic", "subtopic", "source")
        q_conditions = Q()
        for key, values in filters.items():
            if values:
                q_conditions &= Q(**{f"{key.rstrip('s')}__in": values})
        task_queryset = task_queryset.filter(q_conditions) if q_conditions else task_queryset
        if task_queryset.exists():
            tasks = random.sample(list(task_queryset), min(task_count, task_queryset.count()))

    format_type = request.GET.get("format", "portrait")
    with_answers = request.GET.get("with_answers") == "1"
    with_solutions = request.GET.get("with_solutions") == "1"

    processed_tasks = [process_task_for_pdf(task, request, with_solutions, with_answers) for task in tasks]
    html = render_to_string("tasks/print_tasks.html", {
        "tasks": processed_tasks,
        "with_answers": with_answers,
        "with_solutions": with_solutions,
        "format": format_type,
        "request": request,
        "small_images": SMALL_IMAGES,
        "medium_images": MEDIUM_IMAGES,
        "large_image": LARGE_IMAGE,
    })

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="generated_tasks_{uuid}.pdf"'
    pdf_content = asyncio.run(render_pdf_with_playwright(html, get_pdf_options(format_type), f"{request.scheme}://{request.get_host()}"))
    response.write(pdf_content)
    return response

def pdf_cart(request, subject, uuid):
    """PDF для задач из корзины."""
    if not validate_subject(subject):
        return HttpResponse("Неверный предмет", status=404)

    task_ids = request.GET.getlist("task_ids")
    if not task_ids:
        logger.warning("No task_ids provided in pdf_cart")
        return HttpResponse("Не выбраны задания для печати", status=400)

    tasks = Task.objects.filter(subject=subject, unique_id__in=task_ids)
    if not tasks.exists():
        logger.warning(f"No tasks found for task_ids: {task_ids}")
        return HttpResponse("Задания не найдены в базе данных", status=404)

    format_type = request.GET.get("format", "portrait")
    with_answers = request.GET.get("with_answers") == "1"
    with_solutions = request.GET.get("with_solutions") == "1"

    processed_tasks = [process_task_for_pdf(task, request, with_solutions, with_answers) for task in tasks]
    html = render_to_string("tasks/print_cart.html", {
        "tasks": processed_tasks,
        "with_answers": with_answers,
        "with_solutions": with_solutions,
        "format": format_type,
        "request": request,
        "small_images": SMALL_IMAGES,
        "medium_images": MEDIUM_IMAGES,
        "large_image": LARGE_IMAGE,
    })

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="cart_{uuid}.pdf"'
    pdf_content = asyncio.run(render_pdf_with_playwright(html, get_pdf_options(format_type), f"{request.scheme}://{request.get_host()}"))
    response.write(pdf_content)
    return response

def pdf_gentask(request, subject, uuid):
    """PDF для сгенерированных задач по task_ids."""
    if not validate_subject(subject):
        return HttpResponse("Неверный предмет", status=404)

    task_ids = request.GET.getlist("task_ids")
    if not task_ids:
        logger.warning("No task_ids provided in pdf_gentask")
        return HttpResponse("Не выбраны задания для печати", status=400)

    tasks = Task.objects.filter(subject=subject, unique_id__in=task_ids)
    if not tasks.exists():
        logger.warning(f"No tasks found for task_ids: {task_ids}")
        return HttpResponse("Задания не найдены в базе данных", status=404)

    format_type = request.GET.get("format", "portrait")
    with_answers = request.GET.get("with_answers") == "1"
    with_solutions = request.GET.get("with_solutions") == "1"

    processed_tasks = [process_task_for_pdf(task, request, with_solutions, with_answers) for task in tasks]
    html = render_to_string("tasks/print_gentask.html", {
        "tasks": processed_tasks,
        "with_answers": with_answers,
        "with_solutions": with_solutions,
        "format": format_type,
        "request": request,
        "small_images": SMALL_IMAGES,
        "medium_images": MEDIUM_IMAGES,
        "large_image": LARGE_IMAGE,
    })

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="gentask_{uuid}.pdf"'
    pdf_content = asyncio.run(render_pdf_with_playwright(html, get_pdf_options(format_type), f"{request.scheme}://{request.get_host()}"))
    response.write(pdf_content)
    return response

@login_required
@require_http_methods(["POST"])
def toggle_favorite(request, subject):
    """Переключение статуса избранного для задачи."""
    if not validate_subject(subject) or not request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

    task_id = request.POST.get("task_id")
    if not task_id:
        logger.error("Task ID is missing")
        return JsonResponse({"success": False, "error": "Task ID is required"}, status=400)

    try:
        task = Task.objects.get(unique_id=task_id, subject=subject)
        favorite, created = Favorite.objects.get_or_create(user=request.user, task=task)
        if not created:
            favorite.delete()
            is_favorite = False
            logger.debug("Removed from favorites")
        else:
            is_favorite = True
            logger.debug("Added to favorites")
        return JsonResponse({
            "success": True,
            "is_favorite": is_favorite,
            "message": "Задание успешно добавлено в избранное" if is_favorite else "Задание удалено из избранного"
        })
    except Task.DoesNotExist:
        logger.error(f"Task not found: {task_id}")
        return JsonResponse({"success": False, "error": "Task not found"}, status=404)
    except Exception as e:
        logger.error(f"Error in toggle_favorite: {str(e)}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@login_required
def favorite_tasks(request, subject):
    """Список избранных задач."""
    if not validate_subject(subject):
        return HttpResponse("Неверный предмет", status=404)

    tasks = Task.objects.filter(favorited_by__user=request.user, subject=subject).select_related("exam_part", "exam_line", "topic", "subtopic", "source")
    tasks = apply_task_filters(tasks, request.GET)

    per_page = request.GET.get("per_page", 20)
    paginator = Paginator(tasks, per_page)
    page = request.GET.get("page")
    try:
        tasks_page = paginator.page(page)
    except PageNotAnInteger:
        tasks_page = paginator.page(1)
    except EmptyPage:
        tasks_page = paginator.page(paginator.num_pages)

    context = {
        "subject": subject,
        "tasks": tasks_page,
        "exam_parts": ExamPart.objects.filter(subject=subject),
        "topics": Topic.objects.filter(subject=subject),
        "subtopics": Subtopic.objects.filter(subject=subject),
        "exam_lines": ExamLine.objects.filter(subject=subject),
        "sources": Source.objects.filter(subject=subject),
        "per_page": per_page,
        "favorite_task_ids": set(tasks.values_list("unique_id", flat=True)),
    }
    return render(request, "tasks/favorite_tasks.html", context)

def get_fields_by_subject(request):
    if not request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    subject = request.GET.get("subject")
    if not subject or subject not in [s.value for s in ExamSubject]:
        return JsonResponse({"error": "Invalid or missing subject"}, status=400)

    try:
        data = {
            "exam_parts": [{"id": p.id, "name": str(p)} for p in ExamPart.objects.filter(subject=subject)],
            "exam_lines": [{"id": l.id, "name": str(l.number)} for l in ExamLine.objects.filter(subject=subject)],
            "topics": [{"id": t.id, "name": str(t)} for t in Topic.objects.filter(subject=subject)],
            "subtopics": [{"id": s.id, "name": str(s)} for s in Subtopic.objects.filter(subject=subject)],
            "sources": [{"id": s.id, "name": str(s)} for s in Source.objects.filter(subject=subject)],
        }
        logger.debug(f"Fields for subject {subject}: {data}")
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Error in get_fields_by_subject: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

def get_subtopics(request):
    if not request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    topic_id = request.GET.get("topic")
    subject = request.GET.get("subject")
    if not topic_id or not subject or subject not in [s.value for s in ExamSubject]:
        return JsonResponse({"error": "Invalid topic or subject"}, status=400)

    try:
        subtopics = Subtopic.objects.filter(topic_id=topic_id, subject=subject)
        data = {"subtopics": [{"id": s.id, "name": str(s)} for s in subtopics]}
        logger.debug(f"Subtopics for topic {topic_id}, subject {subject}: {data}")
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Error in get_subtopics: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)

def get_all_fields(request):
    """Получение всех полей (для отладки)."""
    if not request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)
    try:
        data = {
            "exam_parts": [{"id": p.id, "name": str(p)} for p in ExamPart.objects.all()],
            "exam_lines": [{"id": l.id, "name": str(l)} for l in ExamLine.objects.all()],
            "topics": [{"id": t.id, "name": str(t)} for t in Topic.objects.all()],
            "subtopics": [{"id": s.id, "name": str(s)} for s in Subtopic.objects.all()],
            "sources": [{"id": s.id, "name": str(s)} for s in Source.objects.all()],
        }
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Error in get_all_fields: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)