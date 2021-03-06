# Generated by Django 3.2.12 on 2022-03-16 06:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_user_last_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=15)),
                ('student_class', models.CharField(max_length=100)),
                ('student_rollno', models.CharField(max_length=20)),
                ('student_marks', models.IntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
