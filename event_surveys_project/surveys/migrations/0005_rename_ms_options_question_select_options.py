# Generated by Django 5.0.6 on 2024-06-19 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0004_question_ms_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='ms_options',
            new_name='select_options',
        ),
    ]