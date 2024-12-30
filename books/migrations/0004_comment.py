# Generated by Django 5.1 on 2024-08-14 09:34

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_rename_book_uuid_readinglist_book_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField(blank=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
            ],
            options={
                'ordering': ['-created_time'],
                'abstract': False,
            },
        ),
    ]