# Generated by Django 5.0.6 on 2024-06-24 14:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0005_rename_ms_options_question_select_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='select_options',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.CreateModel(
            name='SurveyCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completion_date', models.DateTimeField(auto_now_add=True)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='completions', to='surveys.survey')),
            ],
            options={
                'verbose_name': 'Survey Completion',
                'verbose_name_plural': 'Survey Completions',
            },
        ),
        migrations.AddField(
            model_name='response',
            name='survey_completion',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='surveys.surveycompletion'),
            preserve_default=False,
        ),
    ]
