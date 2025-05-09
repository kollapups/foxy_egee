from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from tasks.models import Task, Comment, Favorite
from .forms import UserRegistrationForm
from users.forms import TaskGeneratorForm
from .models import CustomUser, Homework, StudentTeacher, StudentHomework, HomeworkFile
from requests_oauthlib import OAuth2Session
from django.conf import settings
import logging
import base64
import hashlib
from django.utils import timezone
import random
import os
from django.db.models import Q
from django.core.paginator import Paginator

logger = logging.getLogger(__name__)

# Разрешаем HTTP для OAuth2 в режиме разработки
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" if settings.DEBUG else "0"


@login_required
def filter_tasks(request, subject):
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse(
            {"success": False, "error": "Требуется AJAX-запрос"}, status=400
        )

    form = TaskGeneratorForm(subject=subject, data=request.GET)
    if form.is_valid():
        parts = form.cleaned_data.get("parts", [])
        exam_lines = form.cleaned_data.get("exam_lines", [])
        topics = form.cleaned_data.get("topics", [])
        subtopics = form.cleaned_data.get("subtopics", [])
        sources = form.cleaned_data.get("sources", [])

        task_queryset = Task.objects.filter(subject=subject).select_related(
            "exam_part", "exam_line", "topic", "subtopic", "source"
        )
        q_conditions = Q()
        if parts:
            q_conditions &= Q(exam_part__in=parts)
        if exam_lines:
            q_conditions &= Q(exam_line__in=exam_lines)
        if topics:
            q_conditions &= Q(topic__in=topics)
        if subtopics:
            q_conditions &= Q(subtopic__in=subtopics)
        if sources:
            q_conditions &= Q(source__in=sources)

        if q_conditions:
            task_queryset = task_queryset.filter(q_conditions)

        # Пагинация: 10 задач на страницу
        page_number = request.GET.get("page", 1)
        paginator = Paginator(task_queryset, 10)
        page_obj = paginator.get_page(page_number)

        tasks = [
            {
                "id": task.id,
                "unique_id": task.unique_id,
                "text": task.text,
                "image": task.image.url if task.image else None,
                "answer": task.answer,
            }
            for task in page_obj
        ]
        return JsonResponse(
            {
                "success": True,
                "tasks": tasks,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
                "page": page_obj.number,
                "total_pages": paginator.num_pages,
            }
        )
    return JsonResponse(
        {"success": False, "error": "Неверные данные фильтра"}, status=400
    )


def generate_pkce_pair():
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8").rstrip("=")
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .decode("utf-8")
        .rstrip("=")
    )
    return code_verifier, code_challenge


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next", settings.LOGIN_REDIRECT_URL)

        code_verifier, code_challenge = generate_pkce_pair()
        oauth = OAuth2Session(
            settings.CLIENT_ID,
            redirect_uri=settings.REDIRECT_URI,
            scope=["read", "write"],
        )

        response = oauth.post(
            "http://localhost:8001/api/login/",
            data={
                "username": username,
                "password": password,
                "client_id": settings.CLIENT_ID,
                "redirect_uri": settings.REDIRECT_URI,
                "code_challenge": code_challenge,
                "code_challenge_method": "S256",
            },
        )

        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

        if response.status_code == 200:
            data = response.json()
            logger.debug(f"Ответ от /api/login/: {response.text}")
            if "code" in data:
                try:
                    token = oauth.fetch_token(
                        "http://localhost:8001/oauth/token/",
                        code=data["code"],
                        client_secret=settings.CLIENT_SECRET,
                        include_client_id=True,
                        code_verifier=code_verifier,
                        scope="read write",
                    )
                    request.session["oauth_token"] = token

                    user_info_response = oauth.get(
                        "http://localhost:8001/api/userinfo/"
                    )
                    if user_info_response.status_code == 200:
                        user_info = user_info_response.json()
                        user, created = CustomUser.objects.get_or_create(
                            username=user_info["username"]
                        )
                        if created:
                            user.email = user_info.get("email", "")
                            user.set_unusable_password()
                            user.save()
                        login(request, user)
                        logger.info(f"Успешная авторизация: {user.username}")
                        messages.success(request, "Вы успешно вошли!")
                        if is_ajax:
                            return JsonResponse(
                                {"success": True, "redirect_url": next_url}
                            )
                        return redirect(next_url)
                    else:
                        logger.error(
                            f"Ошибка получения userinfo: {user_info_response.text}"
                        )
                        error_msg = "Не удалось получить данные пользователя"
                        if is_ajax:
                            return JsonResponse(
                                {"success": False, "error": error_msg}, status=400
                            )
                        messages.error(request, error_msg)
                except Exception as e:
                    logger.error(f"Ошибка при получении токена: {str(e)}")
                    error_msg = f"Ошибка авторизации: {str(e)}"
                    if is_ajax:
                        return JsonResponse(
                            {"success": False, "error": error_msg}, status=400
                        )
                    messages.error(request, error_msg)
            else:
                error_msg = "Ошибка авторизации: код не получен"
                if is_ajax:
                    return JsonResponse(
                        {"success": False, "error": error_msg}, status=400
                    )
                messages.error(request, error_msg)
        else:
            logger.warning(
                f"Неудачная попытка входа: {username}. Ответ от school: {response.text}"
            )
            error_msg = response.json().get("error", "Неверный логин или пароль")
            if is_ajax:
                return JsonResponse({"success": False, "error": error_msg}, status=400)
            messages.error(request, error_msg)

        if is_ajax:
            return JsonResponse(
                {"success": False, "error": "Ошибка авторизации"}, status=400
            )
        return redirect(next_url)
    return redirect(settings.LOGIN_REDIRECT_URL)


def oauth_callback(request):
    try:
        oauth = OAuth2Session(
            settings.CLIENT_ID,
            redirect_uri=settings.REDIRECT_URI,
            state=request.session.get("oauth_state"),
        )
        token = oauth.fetch_token(
            settings.TOKEN_URL,
            client_secret=settings.CLIENT_SECRET,
            code=request.GET.get("code"),
        )
        request.session["oauth_token"] = token

        user_info_response = oauth.get("http://localhost:8001/api/userinfo/")
        if user_info_response.status_code == 200:
            user_info = user_info_response.json()
            username = user_info["username"]
            email = user_info.get("email", "")
        else:
            raise Exception("Не удалось получить информацию о пользователе")

        user, created = CustomUser.objects.get_or_create(username=username)
        if created:
            user.email = email
            user.set_unusable_password()
            user.save()

        login(request, user)
        logger.info(f"Успешная авторизация: {username}")
        messages.success(request, "Вы успешно вошли!")

        next_url = request.session.get("next_url", settings.LOGIN_REDIRECT_URL)
        return redirect(next_url)
    except Exception as e:
        logger.error(f"Ошибка OAuth2: {str(e)}")
        messages.error(request, "Ошибка авторизации. Попробуйте снова.")
        return redirect(settings.LOGIN_REDIRECT_URL)


@login_required
def logout_view(request):
    try:
        if "oauth_token" in request.session:
            del request.session["oauth_token"]
        logout(request)
        logger.info("Пользователь успешно вышел")
        messages.success(request, "Вы успешно вышли!")
    except Exception as e:
        logger.error(f"Ошибка при выходе: {str(e)}")
        messages.error(request, "Ошибка при выходе.")
    return redirect(settings.LOGOUT_REDIRECT_URL)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            registration_data = {
                "username": form.cleaned_data["username"],
                "email": form.cleaned_data["email"],
                "password": form.cleaned_data["password1"],
                "role": form.cleaned_data["role"],
            }
            request.session["registration_data"] = registration_data

            code_verifier, code_challenge = generate_pkce_pair()
            oauth = OAuth2Session(
                settings.CLIENT_ID,
                redirect_uri=settings.REDIRECT_URI,
                scope=["read", "write"],
            )
            response = oauth.post(
                "http://localhost:8001/api/register/",
                data={
                    "username": registration_data["username"],
                    "email": registration_data["email"],
                    "password": registration_data["password"],
                    "client_id": settings.CLIENT_ID,
                    "redirect_uri": settings.REDIRECT_URI,
                    "code_challenge": code_challenge,
                    "code_challenge_method": "S256",
                },
            )

            if response.status_code == 200:
                data = response.json()
                logger.debug(f"Ответ от /api/register/: {response.text}")
                if "code" in data:
                    try:
                        token = oauth.fetch_token(
                            "http://localhost:8001/oauth/token/",
                            code=data["code"],
                            client_secret=settings.CLIENT_SECRET,
                            include_client_id=True,
                            code_verifier=code_verifier,
                            scope="read write",
                        )
                        request.session["oauth_token"] = token

                        user_info_response = oauth.get(
                            "http://localhost:8001/api/userinfo/"
                        )
                        if user_info_response.status_code == 200:
                            user_info = user_info_response.json()
                            user, created = CustomUser.objects.get_or_create(
                                username=user_info["username"]
                            )
                            if created:
                                user.email = user_info.get("email", "")
                                user.role = registration_data["role"]
                                user.set_unusable_password()
                                user.save()
                            login(request, user)
                            logger.info(f"Успешная регистрация и вход: {user.username}")
                            messages.success(request, "Вы успешно зарегистрированы!")
                            next_url = request.POST.get(
                                "next", settings.LOGIN_REDIRECT_URL
                            )
                            if (
                                request.headers.get("X-Requested-With")
                                == "XMLHttpRequest"
                            ):
                                return JsonResponse(
                                    {"success": True, "redirect_url": next_url}
                                )
                            return redirect(next_url)
                        else:
                            error_msg = "Не удалось получить данные пользователя"
                            logger.error(f"Ошибка userinfo: {user_info_response.text}")
                            if (
                                request.headers.get("X-Requested-With")
                                == "XMLHttpRequest"
                            ):
                                return JsonResponse(
                                    {"success": False, "error": error_msg}, status=400
                                )
                            messages.error(request, error_msg)
                    except Exception as e:
                        logger.error(f"Ошибка при получении токена: {str(e)}")
                        error_msg = f"Ошибка регистрации: {str(e)}"
                        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                            return JsonResponse(
                                {"success": False, "error": error_msg}, status=400
                            )
                        messages.error(request, error_msg)
                else:
                    error_msg = "Код авторизации не получен"
                    logger.error(f"Ошибка в ответе /api/register/: {response.text}")
                    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                        return JsonResponse(
                            {"success": False, "errors": {"__all__": [error_msg]}},
                            status=400,
                        )
                    messages.error(request, error_msg)
            else:
                error_msg = response.json().get("error", "Ошибка регистрации")
                logger.error(f"Ошибка регистрации: {response.text}")
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return JsonResponse(
                        {"success": False, "errors": {"__all__": [error_msg]}},
                        status=400,
                    )
                messages.error(request, error_msg)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {"success": False, "errors": form.errors}, status=400
                )
            messages.error(request, "Ошибка валидации формы")
            return redirect(settings.LOGIN_REDIRECT_URL)
    return redirect(settings.LOGIN_REDIRECT_URL)


@login_required
def toggle_favorite(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, task=task)
    if not created:
        favorite.delete()
    return redirect("users:profile")


@login_required
def update_student_name(request):
    if request.method == "POST" and request.user.role == "teacher":
        student_id = request.POST.get("student_id")
        new_name = request.POST.get("new_name")
        student = get_object_or_404(
            CustomUser, id=student_id, teachers__teacher=request.user
        )
        student.display_name = new_name
        student.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "message": "Ошибка"})


@login_required
def profile(request):
    if request.method == "POST":
        if request.user.role == "student":
            teacher_code = request.POST.get("teacher_code")
            if teacher_code:
                try:
                    teacher = CustomUser.objects.get(
                        teacher_code=teacher_code, role="teacher"
                    )
                    StudentTeacher.objects.get_or_create(
                        student=request.user, teacher=teacher
                    )
                    messages.success(request, "Вы успешно привязаны к учителю!")
                except CustomUser.DoesNotExist:
                    messages.error(request, "Учитель с таким кодом не найден.")
            return redirect("users:profile")
        elif request.user.role == "teacher":
            request.user.first_name = request.POST.get("first_name", "")
            request.user.last_name = request.POST.get("last_name", "")
            request.user.specialty = request.POST.get("specialty", "")
            request.user.save()
            messages.success(request, "Профиль обновлён!")
            return redirect("users:profile")

    subject = request.GET.get("subject", "math")
    context = {
        "user": request.user,
        "teacher_code": (
            request.user.teacher_code if request.user.role == "teacher" else None
        ),
        "favorite_tasks": request.user.favorite_tasks.filter(task__subject=subject),
        "comments": (
            request.user.comments.filter(task__subject=subject)
            if request.user.is_authenticated
            else []
        ),
        "subject": subject,
    }

    if request.user.role == "teacher":
        context["students"] = CustomUser.objects.filter(
            student_teachers__teacher=request.user
        )
        context["assigned_homeworks"] = Homework.objects.filter(teacher=request.user)
    elif request.user.role == "student":
        context["teachers"] = CustomUser.objects.filter(
            teacher_students__student=request.user
        )
        context["received_homeworks"] = (
            StudentHomework.objects.filter(student=request.user)
            .select_related("homework__teacher")
            .prefetch_related("homework__tasks")
        )

    return render(request, "users/profile.html", context)


@login_required
def create_homework(request, subject):
    if request.user.role != "teacher":
        return redirect("users:profile")

    homework_type = request.GET.get("homework_type") or request.POST.get(
        "homework_type"
    )
    form = TaskGeneratorForm(
        subject=subject, homework_type=homework_type, data=request.GET or None
    )
    tasks = []
    error_message = None
    selected_tasks = request.session.get("selected_tasks", [])

    # Обработка AJAX-запросов
    if (
        request.method == "POST"
        and request.headers.get("X-Requested-With") == "XMLHttpRequest"
    ):
        task_id = request.POST.get("task_id")
        if "add_task" in request.POST:
            try:
                task = Task.objects.get(unique_id=task_id, subject=subject)
                if task_id not in selected_tasks:
                    selected_tasks.append(task_id)
                    request.session["selected_tasks"] = selected_tasks
                    return JsonResponse({"success": True, "task_text": task.text[:30]})
                return JsonResponse(
                    {"success": False, "error": "Задание уже в корзине"}
                )
            except Task.DoesNotExist:
                return JsonResponse({"success": False, "error": "Задание не найдено"})
        elif "remove_task" in request.POST:
            if task_id in selected_tasks:
                selected_tasks.remove(task_id)
                request.session["selected_tasks"] = selected_tasks
                return JsonResponse({"success": True})
            return JsonResponse({"success": False, "error": "Задание не в корзине"})
        elif "refresh_task" in request.POST:
            if task_id in selected_tasks:
                task_queryset = Task.objects.filter(subject=subject).exclude(
                    unique_id__in=selected_tasks
                )
                if task_queryset.exists():
                    new_task = random.choice(list(task_queryset))
                    selected_tasks[selected_tasks.index(task_id)] = new_task.unique_id
                    request.session["selected_tasks"] = selected_tasks
                    return JsonResponse(
                        {
                            "success": True,
                            "new_task_id": new_task.unique_id,
                            "task_text": new_task.text[:30],
                        }
                    )
                return JsonResponse(
                    {"success": False, "error": "Нет доступных заданий для замены"}
                )
            return JsonResponse({"success": False, "error": "Задание не в корзине"})
        elif "delete_homework" in request.POST:
            homework_id = request.POST.get("homework_id")
            try:
                homework = Homework.objects.get(id=homework_id, teacher=request.user)
                homework.delete()
                return JsonResponse({"success": True})
            except Homework.DoesNotExist:
                return JsonResponse(
                    {"success": False, "error": "Домашнее задание не найдено"}
                )
        elif "clear_cart" in request.POST:
            request.session["selected_tasks"] = []
            return JsonResponse({"success": True})

    # Сохранение ДЗ
    if request.method == "POST" and "save_homework" in request.POST:
        title = request.POST.get("title")
        if not title:
            title = f"ДЗ №{Homework.objects.filter(teacher=request.user).count() + 1}"
        description = request.POST.get("description", "")
        due_date = request.POST.get("due_date") or None
        student_ids = request.POST.getlist("students")
        image_size = request.POST.get("image_size", "150")

        if not student_ids:
            messages.error(request, "Выберите хотя бы одного ученика")
            return redirect("users:create_homework", subject=subject)

        homework = Homework.objects.create(
            teacher=request.user,
            title=title,
            description=description,
            due_date=due_date,
            homework_type=homework_type,
            image_size=image_size,
        )

        if homework_type == "upload":
            if "task_files" in request.FILES:
                files = request.FILES.getlist("task_files")
                if len(files) > 10:
                    homework.delete()
                    messages.error(request, "Максимум 10 файлов")
                    return redirect("users:create_homework", subject=subject)
                for file in files:
                    if file.size > 5 * 1024 * 1024:
                        homework.delete()
                        messages.error(request, f"Файл {file.name} превышает 5 МБ")
                        return redirect("users:create_homework", subject=subject)
                    HomeworkFile.objects.create(homework=homework, file=file)
            answers = {
                key.split("[")[1].rstrip("]"): value
                for key, value in request.POST.items()
                if key.startswith("answers[")
            }
            homework.answers = answers if answers else None

        elif homework_type in ["manual", "random"]:
            if not selected_tasks:
                homework.delete()
                messages.error(request, "Выберите хотя бы одно задание")
                return redirect("users:create_homework", subject=subject)
            homework.tasks.set(Task.objects.filter(unique_id__in=selected_tasks))
            request.session["selected_tasks"] = []

        homework.students.set(CustomUser.objects.filter(id__in=student_ids))
        for student_id in student_ids:
            StudentHomework.objects.get_or_create(
                student_id=student_id,
                homework=homework,
                defaults={"status": "pending"},
            )
        homework.save()
        messages.success(request, "Домашнее задание успешно создано!")
        return redirect("users:profile")

    selected_students = request.GET.getlist("students", [])

    # Фильтрация для GET-запроса (manual и random)
    if (
        request.method == "GET"
        and homework_type in ["manual", "random"]
        and form.is_valid()
    ):
        parts = form.cleaned_data.get("parts", [])
        exam_lines = form.cleaned_data.get("exam_lines", [])
        topics = form.cleaned_data.get("topics", [])
        subtopics = form.cleaned_data.get("subtopics", [])
        sources = form.cleaned_data.get("sources", [])
        search_text = request.GET.get("search_text", "").strip()
        task_count = (
            int(request.GET.get("task_count", 1)) if homework_type == "random" else 10
        )

        task_queryset = Task.objects.filter(subject=subject).select_related(
            "exam_part", "exam_line", "topic", "subtopic", "source"
        )
        q_conditions = Q()
        if parts:
            q_conditions &= Q(exam_part__in=parts)
        if exam_lines:
            q_conditions &= Q(exam_line__in=exam_lines)
        if topics:
            q_conditions &= Q(topic__in=topics)
        if subtopics:
            q_conditions &= Q(subtopic__in=subtopics)
        if sources:
            q_conditions &= Q(source__in=sources)
        if search_text:
            q_conditions &= Q(text__icontains=search_text)

        if q_conditions:
            task_queryset = task_queryset.filter(q_conditions)
            if not task_queryset.exists():
                error_message = "Нет заданий, соответствующих выбранным фильтрам."
        else:
            task_queryset = task_queryset

        if task_queryset.exists():
            if homework_type == "random":
                random_tasks = random.sample(
                    list(task_queryset), min(task_count, task_queryset.count())
                )
                selected_tasks = [task.unique_id for task in random_tasks]
                request.session["selected_tasks"] = selected_tasks
                tasks = random_tasks  # Для отображения в контексте
            else:  # manual
                paginator = Paginator(task_queryset, 10)
                page_number = request.GET.get("page", 1)
                tasks = paginator.get_page(page_number)
        else:
            error_message = "Нет заданий, соответствующих выбранным фильтрам."

    context = {
        "subject": subject,
        "form": form,
        "tasks": tasks,
        "error_message": error_message,
        "students": CustomUser.objects.filter(student_teachers__teacher=request.user),
        "assigned_homeworks": Homework.objects.filter(teacher=request.user),
        "homework_type": homework_type,
        "selected_tasks": Task.objects.filter(unique_id__in=selected_tasks),
        "selected_students": selected_students,
    }
    return render(request, "users/teacher_homework.html", context)


@login_required
def get_homework(request, subject):
    if request.user.role != "student":
        return redirect("users:profile")  # Перенаправляем, если не ученик

    if (
        request.method == "GET"
        and request.headers.get("X-Requested-With") == "XMLHttpRequest"
    ):
        homework_id = request.GET.get("homework_id")
        student_homework = get_object_or_404(
            StudentHomework, id=homework_id, student=request.user
        )
        homework = student_homework.homework

        response = {
            "success": True,
            "title": homework.title,
            "homework_type": homework.homework_type,
            "image_size": homework.image_size,
            "description": homework.description,
            "due_date": homework.due_date.isoformat() if homework.due_date else None,
            "status": student_homework.status,
        }
        if homework.homework_type == "upload":
            files = homework.files.all()
            if files:
                response["file_urls"] = [
                    {"url": file.file.url, "name": file.file.name} for file in files
                ]
            response["answers"] = homework.answers or {}
        elif homework.homework_type in ["manual", "random"]:
            response["tasks"] = [
                {
                    "id": task.id,
                    "unique_id": task.unique_id,
                    "text": task.text,
                    "image": task.image.url if task.image else None,
                    "can_answer": bool(task.answer),
                }
                for task in homework.tasks.all()
            ]
        return JsonResponse(response)

    context = {
        "subject": subject,
        "received_homeworks": (
            StudentHomework.objects.filter(student=request.user)
            .select_related("homework__teacher")
            .prefetch_related("homework__tasks")
        ),
    }
    return render(request, "users/student_homework.html", context)


@login_required
def submit_homework(request, subject):
    if request.user.role != "student":
        return JsonResponse({"success": False, "error": "Доступ запрещён"}, status=403)

    if request.method == "POST":
        homework_id = request.POST.get("homework_id")
        student_homework = get_object_or_404(
            StudentHomework, id=homework_id, student=request.user
        )
        homework = student_homework.homework

        if student_homework.status == "completed":
            return JsonResponse({"success": False, "error": "ДЗ уже сдано"}, status=400)

        if homework.due_date and timezone.now() > homework.due_date:
            return JsonResponse(
                {"success": False, "error": "Срок сдачи истёк"}, status=400
            )

        if homework.homework_type == "upload":
            if "submission_file" in request.FILES:
                if request.FILES["submission_file"].size > 2 * 1024 * 1024:
                    return JsonResponse(
                        {"success": False, "error": "Файл превышает 2 МБ"}, status=400
                    )
                student_homework.submission_file = request.FILES["submission_file"]
                student_homework.status = "completed"
                student_homework.submitted_at = timezone.now()
                student_homework.save()
                return JsonResponse(
                    {"success": True, "message": "ДЗ сдано, ожидает проверки"}
                )
            elif homework.answers:
                student_answers = {
                    key.split("[")[1].rstrip("]"): value
                    for key, value in request.POST.items()
                    if key.startswith("student_answers[")
                }
                results = {}
                for task_num, correct_answer in homework.answers.items():
                    student_answer = student_answers.get(task_num, "")
                    results[task_num] = {
                        "student_answer": student_answer,
                        "correct_answer": correct_answer,
                    }
                student_homework.results = results
                student_homework.status = "completed"
                student_homework.submitted_at = timezone.now()
                student_homework.save()
                return JsonResponse({"success": True, "results": results})

        elif homework.homework_type in ["manual", "random"]:
            student_answers = {
                key.split("[")[1].rstrip("]"): value
                for key, value in request.POST.items()
                if key.startswith("student_answers[")
            }
            results = {}
            for task in homework.tasks.all():
                if task.answer:
                    student_answer = student_answers.get(str(task.id), "")
                    results[task.unique_id] = {
                        "student_answer": student_answer,
                        "correct_answer": task.answer,
                    }
            student_homework.results = results
            student_homework.status = "completed"
            student_homework.submitted_at = timezone.now()
            student_homework.save()
            return JsonResponse({"success": True, "results": results})

        return JsonResponse(
            {"success": False, "error": "Ошибка при сдаче ДЗ"}, status=400
        )
    return JsonResponse(
        {"success": False, "error": "Требуется POST-запрос"}, status=400
    )


@login_required
def homework_results(request, subject, homework_id, student_id):
    if request.user.role != "teacher":
        return JsonResponse({"success": False, "error": "Доступ запрещён"}, status=403)

    homework = get_object_or_404(Homework, id=homework_id, teacher=request.user)
    student = get_object_or_404(CustomUser, id=student_id)
    student_hw = get_object_or_404(StudentHomework, homework=homework, student=student)

    context = {
        "homework": homework,
        "student": student,
        "results": student_hw.results,
        "submission_file": (
            student_hw.submission_file.url if student_hw.submission_file else None
        ),
    }
    return render(request, "users/homework_results.html", context)


@login_required
def homework_detail(request, subject, homework_id):
    homework = get_object_or_404(Homework, id=homework_id, teacher=request.user)
    student_submissions = StudentHomework.objects.filter(
        homework=homework
    ).select_related("student")
    context = {
        "homework": homework,
        "student_submissions": student_submissions,
        "subject": subject,
    }
    return render(request, "users/homework_detail.html", context)
