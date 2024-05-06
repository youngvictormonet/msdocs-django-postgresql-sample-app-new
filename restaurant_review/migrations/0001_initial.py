import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('street_address', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20)),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('review_text', models.CharField(max_length=500)),
                ('review_date', models.DateTimeField(verbose_name='review date')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant_review.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitter', models.CharField(max_length=250)),
                ('email', models.EmailField()),
                ('ordinals_address', models.CharField(max_length=250)),
                ('points', models.IntegerField()),
                ('ref_status', models.BooleanField()),
                ('date_created', models.DateTimeField()),
                ('date_updated', models.DateTimeField()),
                ('tweet_link', models.CharField(max_length=250)),
                ('wl', models.BooleanField()),
                ('fcfs', models.BooleanField()),
                ('invitation_code', models.CharField(max_length=250)),
            ],
        ),
    ]
