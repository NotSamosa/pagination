from rest_framework import generics
from articles.models import Article
from articles.serializers import ArticleSerializer

class ArticleListAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.filter(is_published=True).order_by('-created_at')
