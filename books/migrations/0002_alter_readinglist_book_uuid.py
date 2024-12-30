# Generated by Django 5.1 on 2024-08-12 13:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readinglist',
            name='book_uuid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reading_lists', to='books.book'),
        ),
    ]