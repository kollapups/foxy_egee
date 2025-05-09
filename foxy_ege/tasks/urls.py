from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    # Существующие маршруты
    path(
        "tasks/get_fields_by_subject/",
        views.get_fields_by_subject,
        name="admin_get_fields_by_subject",
    ),
    path(
        "tasks/get_subtopics/",
        views.get_subtopics,
        name="admin_get_subtopics",
    ),
    path("", views.home, name="home"),
    path("<str:subject>/", views.home, name="subject_home"),
    path("<str:subject>/tasks/", views.task_list, name="task_list"),
    path("<str:subject>/task/<str:unique_id>/", views.task_detail, name="task_detail"),
    path("<str:subject>/favorite_tasks/", views.favorite_tasks, name="favorite_tasks"),
    path(
        "<str:subject>/generate_variant/",
        views.generate_variant,
        name="generate_variant",
    ),
    path(
        "<str:subject>/variant/<str:variant_id>/",
        views.generate_variant_with_id,
        name="generate_variant_with_id",
    ),
    path("<str:subject>/generate_task/", views.generate_task, name="generate_task"),
    path("<str:subject>/print_settings/", views.print_settings, name="print_settings"),
    path(
        "<str:subject>/print_variants_settings/<str:uuid>/",
        views.print_variants_settings,
        name="print_variants_settings",
    ),
    path("<str:subject>/pdf/tasks/<str:uuid>/", views.pdf_tasks, name="pdf_tasks"),
    path(
        "<str:subject>/pdf/variant/<str:uuid>/<str:variant_id>/",
        views.pdf_variant,
        name="pdf_variant",
    ),
    path(
        "<str:subject>/pdf/generated_tasks/<str:uuid>/",
        views.pdf_generated_tasks,
        name="pdf_generated_tasks",
    ),
    path(
        "<str:subject>/toggle_favorite/", views.toggle_favorite, name="toggle_favorite"
    ),
    # Новые маршруты для корзины
    path(
        "<str:subject>/print_settings_cart/",
        views.print_settings_cart,
        name="print_settings_cart",
    ),
    path("<str:subject>/pdf_cart/<str:uuid>/", views.pdf_cart, name="pdf_cart"),
    # Новые маршруты для generate_task
    path(
        "<str:subject>/print_settings_gentask/",
        views.print_settings_gentask,
        name="print_settings_gentask",
    ),
    path(
        "<str:subject>/pdf_gentask/<str:uuid>/", views.pdf_gentask, name="pdf_gentask"
    ),
    # path("<str:subject>/statistics/", views.visit_statistics, name="visit_statistics"),
]