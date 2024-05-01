
from django_filters import FilterSet
from restaurant_review.models import Users

class UsersFilter(FilterSet):
    class Meta:
        model = Users
        fields = {"twitter": ["exact"]}


