from rest_framework.generics import ListAPIView
from .models import News
from .serializers import NewsSerializer
from django.db.models import Q

class NewsList(ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        queryset = News.objects.all()

        tags_param = self.request.query_params.get('tags', None)
        if tags_param:
            tags = tags_param.split(',')
            query_tags = Q()
            for tag in tags:
                query_tags |= Q(tags__icontains=tag)
            queryset = queryset.filter(query_tags)

        keywords_param = self.request.query_params.get('keywords', None)
        if keywords_param:
            keywords = keywords_param.split(',')
            query_keywords = Q()
            for kw in keywords:
                query_keywords |= Q(title__icontains=kw) | Q(content__icontains=kw)
            queryset = queryset.filter(query_keywords)

        exclude_keywords_param = self.request.query_params.get('exclude_keywords', None)
        if exclude_keywords_param:
            exclude_keywords = exclude_keywords_param.split(',')
            exclude_query = Q()
            for kw in exclude_keywords:
                exclude_query |= Q(title__icontains=kw) | Q(content__icontains=kw)
            queryset = queryset.exclude(exclude_query)

        return queryset
