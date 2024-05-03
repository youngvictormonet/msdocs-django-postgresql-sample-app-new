import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant_review", "0001_initial"),
    ]

    operations = [
        migrations.AddField (
            model_name="users",
            name="invitation_code",
            field=models.CharField(max_length=250)
        ),
    ]
