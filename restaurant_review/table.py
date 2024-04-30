import django_tables2 as tables
from restaurant_review.models import Users

class UsersHTMxTable(tables.Table):
    class Meta:
        model = Users
        template_name = "django_tables2/bootstrap4.html"

