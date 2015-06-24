from django.conf import settings
from django.utils import translation
from chattyhive_project.settings import common_settings

class AdminLocaleMiddleware:

    def process_request(self, request):
        if request.path.startswith('/admin'):
            request.LANG = getattr(common_settings, 'ADMIN_LANGUAGE_CODE',
                                   common_settings.LANGUAGE_CODE)
            translation.activate(request.LANG)
            request.LANGUAGE_CODE = request.LANG
