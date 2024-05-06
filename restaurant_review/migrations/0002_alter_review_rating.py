import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant_review", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="rating",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(5),
                ]
            ),
        ),
    ]
