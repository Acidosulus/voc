from django.db import models

# Create your models here.
class Syllable(models.Model):
    word = models.TextField( verbose_name = 'Слово', default = '', unique = True, primary_key=True)
    transcription = models.TextField(null=True, verbose_name = 'Транскрипция', default = '', blank=True)
    translations = models.TextField(null=True, verbose_name = 'Переводы', default = '', blank=True)
    examples = models.TextField(null=True, verbose_name = 'Примеры', default = '', blank=True)
    show_count =models.IntegerField(null=True, verbose_name = 'Количество показов', default = 0)
    ready = models.IntegerField(null=True, verbose_name = 'Признак выученности', default = 0)
    last_view = models.DateTimeField(null=True, verbose_name='Дата/Время последнего просмотра', auto_now_add = True)

class Books(models.Model):
    id_book = models.AutoField(primary_key=True)
    book_name = models.TextField(null=True, verbose_name = 'Название книги', default = '', blank=True)
    current_paragraph = models.IntegerField(null=True, verbose_name='Текущий читаемый параграф', default=1)

class Paragraphs(models.Model):
    id_paragraph = models.AutoField(primary_key=True)
    id_book = models.IntegerField(null=True, verbose_name = 'Идентификатор книги', default = 0, blank=True)
    paragraph = models.TextField(null=True, verbose_name = 'Параграф книги', default = '', blank=True)

