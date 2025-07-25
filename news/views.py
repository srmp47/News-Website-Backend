from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from .NewsFilter import NewsFilter
from .models import News
from .serializers import NewsSerializer

class NewsList(ListAPIView):
    queryset = News.objects.all().prefetch_related('tags').order_by('-id')
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter
