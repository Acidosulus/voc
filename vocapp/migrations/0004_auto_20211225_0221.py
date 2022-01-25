# Generated by Django 3.2.10 on 2021-12-24 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocapp', '0003_syllable_last_view'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syllable',
            name='examples',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Примеры'),
        ),
        migrations.AlterField(
            model_name='syllable',
            name='transcription',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Транскрипция'),
        ),
        migrations.AlterField(
            model_name='syllable',
            name='translations',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Переводы'),
        ),
    ]