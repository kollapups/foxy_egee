from tasks.models import PageVisit

def page_visit(request):
    # Получаем статистику для текущего URL (без параметров)
    url = request.path
    visit = PageVisit.objects.filter(url=url, is_bot=False).first()
    return {
        'page_visit': visit,
    }