from django.db.models import F
from tasks.models import PageVisit
import re

class VisitCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Список паттернов для выявления ботов по User-Agent
        self.bot_patterns = [
            r'bot', r'crawler', r'spider', r'googlebot', r'yandexbot', r'bingbot',
            r'baiduspider', r'slurp', r'duckduckbot', r'facebookexternalhit',
            r'twitterbot', r'linkedinbot', r'ahrefsbot', r'mj12bot',
        ]
        self.bot_regex = re.compile('|'.join(self.bot_patterns), re.IGNORECASE)

    def __call__(self, request):
        # Пропускаем запросы к админке, статике и медиа
        if request.path.startswith(('/admin/', '/static/', '/media/')):
            return self.get_response(request)

        # Определяем, является ли запрос ботом
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        is_bot = bool(self.bot_regex.search(user_agent))

        # Нормализуем URL (удаляем параметры запроса)
        url = request.path

        # Обновляем или создаем запись посещения
        visit, created = PageVisit.objects.get_or_create(
            url=url,
            is_bot=is_bot,
            defaults={'visit_count': 1}
        )
        if not created:
            PageVisit.objects.filter(id=visit.id).update(
                visit_count=F('visit_count') + 1
            )

        return self.get_response(request)