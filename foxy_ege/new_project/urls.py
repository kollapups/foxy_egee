from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from tasks.sitemaps import TaskSitemap, SubjectStaticSitemap, GlobalStaticSitemap
# from tasks.views import accept_cookies, decline_cookies, delete_cookies

sitemaps = {
    'tasks': TaskSitemap,
    'subject_static': SubjectStaticSitemap,
    'global_static': GlobalStaticSitemap,
}

urlpatterns = [
    # path('privacy-policy/', TemplateView.as_view(template_name='privacy_policy.html'), name='privacy_policy'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('users/', include('users.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # path('cookie_consent/', include('cookie_consent.urls')),
    # path('accept-cookies/', accept_cookies, name='accept_cookies'),
    # path('decline-cookies/', decline_cookies, name='decline_cookies'),
    # path('delete-cookies/', delete_cookies, name='delete_cookies'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)