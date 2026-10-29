from django.apps import AppConfig
from rest_framework.pagination import PageNumberPagination

class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'articles'

    def ready(self):
        PageNumberPagination.page_size_query_param = 'page_size'
        PageNumberPagination.max_page_size = 50
