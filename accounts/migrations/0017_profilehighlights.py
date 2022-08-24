# Generated by Django 4.0.4 on 2022-08-24 04:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_customuser_follower_customuser_following'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileHighlights',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('highlight', models.URLField(blank=True, default='https://www.youtube.com/watch?v=dQw4w9WgXcQ', null=True)),
                ('feedback', models.ManyToManyField(blank=True, related_name='feedback', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
