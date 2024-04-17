from django.db.models import Q
import django_filters
from .models import Users

class UsersFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search', label="")

    class Meta:
        model = Users
        fields = ['query']

    def universal_search(self, queryset, name, value):
        return Users.objects.filter(
            Q(twitter__icontains=value) | Q(email__icontains=value)
        )

