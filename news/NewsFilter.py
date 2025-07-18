import django_filters
from django.db.models import Q
from .models import News

class NewsFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(
        method='filter_tags',
        label='Tags (comma separated)'
    )
    keywords = django_filters.CharFilter(
        method='filter_keywords',
        label='Search in title/content'
    )
    exclude_keywords = django_filters.CharFilter(
        method='filter_exclude_keywords',
        label='Exclude words'
    )

    class Meta:
        model  = News
        fields = []

    def filter_tags(self, queryset, tag_string, value):
        tags = [t.strip() for t in value.split(',') if t.strip()]
        q = Q()
        for tag in tags:
            q |= Q(tags__tag_string__icontains=tag)
        return queryset.filter(q).distinct()

    def filter_keywords(self, queryset, tag_string, value):
        kws = [k.strip() for k in value.split(',') if k.strip()]
        q = Q()
        for kw in kws:
            q |= Q(title__icontains=kw) | Q(content__icontains=kw)
        return queryset.filter(q)

    def filter_exclude_keywords(self, queryset, tag_string, value):
        exs = [e.strip() for e in value.split(',') if e.strip()]
        q = Q()
        for e in exs:
            q |= Q(title__icontains=e) | Q(content__icontains=e)
        return queryset.exclude(q)
