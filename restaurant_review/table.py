import django_tables2 as tables
from .models import Users

class UsersHTMxTable(tables.Table):
    class Meta:
        model = Users
        template_name = "restaurant_review/bootstrap_htmx.html"

