from django.urls import path
from articles.views import ArticleListAPIView

urlpatterns = [
    path('articles/', ArticleListAPIView.as_view(), name='article-list'),
]

