# Generated by Django 5.0.6 on 2024-06-25 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0006_alter_question_select_options_surveycompletion_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['position'], 'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.AddField(
            model_name='question',
            name='position',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
