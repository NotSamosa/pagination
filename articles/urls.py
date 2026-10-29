from django.urls import path
from articles.views import ArticleListAPIView, CustomArticleListAPIView

urlpatterns = [
    path('articles/', ArticleListAPIView.as_view(), name='article-list'),
    path('articles/custom/', CustomArticleListAPIView.as_view(), name='article-list-custom'),
]
