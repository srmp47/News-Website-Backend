from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from .NewsFilter import NewsFilter
from .models import News
from .serializers import NewsSerializer

class NewsList(ListAPIView):
    queryset = News.objects.all()                   # ← Base queryset
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend]         # ← Tell DRF you’re using django-filter
    filterset_class = NewsFilter                    # ← Point at your custom FilterSet
