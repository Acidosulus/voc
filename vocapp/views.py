from django.shortcuts import render, redirect
from django import forms
from .models import Syllable,Books,Paragraphs
#import sqlite3 as sl
import datetime
from datetime import date, timedelta
import load_syllable_from_wooordhunt
import os.path
import subprocess
import re
import hashlib
import threading

def test(request):
    return
    print(" ============== test")
    pc_file_path = r'C:\voc\voc\Blood_of_the_Fold_by_Terry_Goodkind_Goodkind,_Terry_z_lib_org.txt'
    lc_book_name = 'Blood of the Fold by Terry Goodkind'
    ll_book = open(pc_file_path, "r", encoding='utf8').readlines()
    lc_result = ''
    for lc_paragraph in ll_book:
        lc_result = lc_result + lc_paragraph.replace(chr(13), '').replace(chr(10), '').replace(chr(12), '')+chr(13)
    lc_result = lc_result.replace(chr(13)+chr(13),chr(13)).replace(chr(13)+chr(13),chr(13)).replace(chr(13)+chr(13),chr(13)).replace(chr(13)+chr(13),chr(13)).replace(chr(13)+chr(13),chr(13)).replace(chr(13)+chr(13),chr(13)).replace(chr(13)+chr(13),chr(13)).replace(chr(13)+chr(13),chr(13)).replace(chr(13)+chr(13),chr(13))
    ll_paragraps = lc_result.split(chr(13))

    book = Books(book_name = lc_book_name, current_paragraph = 1)
    book.save()


    for lc_p in ll_paragraps:
        print('==============================================')
        print(lc_p)
        if len(lc_p):
            paragraph = Paragraphs(id_book = book.id_book, paragraph = lc_p)
            paragraph.save()

    data = {"text":lc_result}
    return render(request, "test.html", context=data)


def index(request):
    print(" ============== index")
    syllable = Syllable.objects.filter(ready=0).order_by('last_view')
    data = {"words":syllable,"number_of_words_to_study":str(len(syllable)), 'number_of_words_learned':str(len(Syllable.objects.filter(ready=1))), "last_added_word":Syllable.objects.filter(ready=0).filter(show_count=0).order_by('-last_view')[0].word}
    return render(request, "index.html", context=data)

def ready_list(request):
    print(" ============== ready_list")
    syllable = Syllable.objects.filter(ready=1).order_by('last_view')
    data = {"words":syllable,"number_of_words_to_study":str(len(syllable)), 'number_of_words_learned':str(len(Syllable.objects.filter(ready=1))), "last_added_word":Syllable.objects.filter(ready=0).filter(show_count=0).order_by('-last_view')[0].word}
    return render(request, "ready_list.html", context=data)

# 'onchange':"document.getElementById('id_link_on_wooordhunt').href='https://wooordhunt.ru/word/'+escape(this.value)"
class UserForm(forms.Form):
    word = forms.CharField( label="Слово", widget=forms.TextInput(attrs={'class' : 'my_class_input_word'}))
    transcription = forms.CharField(label="Транскрипция", widget=forms.TextInput(attrs={'class' : 'my_class_input_transcription'} ))
    translations = forms.CharField(label="Перевод", widget=forms.Textarea(attrs={'class' : 'my_class_input_translations','rows':"7"} ))
    examples = forms.CharField(label="Примеры", widget=forms.Textarea(attrs={'class':"my_class_input_examples",'rows':"7"} ))





def add_new_with_parameter(request, pc_new_word):
    if request.method == "POST":
        if len(request.POST.get("translations"))>0:
            syllable = Syllable(word = request.POST.get("word").lower(), transcription = request.POST.get("transcription"), translations = request.POST.get("translations"), examples = request.POST.get("examples"), last_view = datetime.datetime.now())
            print(syllable.word, syllable.transcription, syllable.translations, syllable.examples, syllable.last_view)
            if len(syllable.word)>=3 and len(syllable.translations)>3:
                syllable.save()
                return redirect(index)
    lo_syllabble = Syllable.objects.get(word=pc_new_word)
    print(" >============== add_new_with_parameter:", pc_new_word, lo_syllabble)
    data = {"word":lo_syllabble.word, "transcription":lo_syllabble.transcription, "translations":lo_syllabble.translations, "examples":lo_syllabble.examples,"number_of_words_to_study":str(len(Syllable.objects.filter(ready=0))), 'number_of_words_learned':str(len(Syllable.objects.filter(ready=1))), "last_added_word":Syllable.objects.filter(ready=0).filter(show_count=0).order_by('-last_view')[0].word}
    return render(request, "add_new.html", context=data)


def add_new(request):
    print(" ====================add_new(request)")
    data = {'word': "", 'transcription': "", 'translations': "", 'examples': "", 'last_view': "","number_of_words_to_study":str(len(Syllable.objects.filter(ready=0))), 'number_of_words_learned':str(len(Syllable.objects.filter(ready=1))), "last_added_word":Syllable.objects.filter(ready=0).filter(show_count=0).order_by('-last_view')[0].word}
    if request.method == "POST":
        print("Количество полученных данных: ", len(Syllable.objects.filter(word=request.POST.get("word").lower())))
        if len(Syllable.objects.filter(word=request.POST.get("word").lower(), ready = 0))>0: # в том случае если слово уже есть в базе, загружаем его, а не загружаем
            return redirect(add_new_with_parameter, request.POST.get("word").lower())
        if len(request.POST.get("translations"))>0:
            syllable = Syllable(word = request.POST.get("word").lower(), transcription = request.POST.get("transcription"), translations = request.POST.get("translations"), examples = request.POST.get("examples"), last_view = datetime.datetime.now())
            print(syllable.word, syllable.transcription, syllable.translations, syllable.examples, syllable.last_view)
            if len(syllable.word)>=3 and len(syllable.translations)>3:
                syllable.save()
                return redirect(index)
        else:
            if len(request.POST.get("word"))>0:
                print(" ============== load_from_wooordhunt")
                print("load_from_wooordhunt:", request.POST.get("word"))
                #try:
                lo_wh = load_syllable_from_wooordhunt.Wooordhunt(r'https://wooordhunt.ru/word/' + request.POST.get("word").lower())
                data = {"word": request.POST.get("word").lower(), "transcription": lo_wh.get_transcription(),
                            "translations": lo_wh.get_translation(),
                            "examples": lo_wh.get_examples(),"number_of_words_to_study":str(len(Syllable.objects.filter(ready=0))), 'number_of_words_learned':str(len(Syllable.objects.filter(ready=1))), "last_added_word":Syllable.objects.filter(ready=0).order_by('-last_view')[0].word}
    else:
        if request.POST.get("word") != None:
            data = {'word':request.POST.get("word").lower(), transcription:'', translations:'', examples:'', last_view:'',"number_of_words_to_study":str(len(Syllable.objects.filter(ready=0))), 'number_of_words_learned':str(len(Syllable.objects.filter(ready=1))), "last_added_word":Syllable.objects.filter(ready=0).order_by('-last_view')[0].word }
        else:
            data = {'word':"", 'transcription':"", 'translations':"", 'examples':"", 'last_view':"","number_of_words_to_study":str(len(Syllable.objects.filter(ready=0))), 'number_of_words_learned':str(len(Syllable.objects.filter(ready=1))), "last_added_word":Syllable.objects.filter(ready=0).order_by('-last_view')[0].word}
    print('||||||||||||||||||||||||', data)
    return render(request, "add_new.html", context=data)



def add_format_for_russian(pc_source:str, lc_style_name): #возвращает строку, где русские символы переданной строки отмечены указанным стилем
    lc_russian = 'йцукенгшщзхъфывапролджэячсмитьбюё'
    lc_russian = lc_russian+lc_russian.upper()
    lc_result = ''
    for lc_chr in pc_source:
        if lc_chr in lc_russian:
            lc_result = lc_result + '<span class = "' + lc_style_name+'">' + lc_chr + '</span>'
        else:
            lc_result = lc_result + lc_chr
    return lc_result


def DownLoadExamples(pl_list):
    path_for_sounds = r'.\\vocapp\\static\\sounds\\examples\\'
    for part in pl_list:
        lc_example = part.split('\n')
        if len(lc_example[0])>10:
            lc_file_name = load_syllable_from_wooordhunt.Delete_from_String_all_Characters_Unsuitable_For_FileName(lc_example[0])
            lc_full_file_name = path_for_sounds + lc_file_name + '.mp3'
            if not os.path.exists(lc_full_file_name):
                try:
                    subprocess.run(["gtts-cli", lc_example[0], "--output", lc_full_file_name])
                    print('saved:', lc_full_file_name)
                except:
                    pass

def word_in_progress(request, pc_word):
    print(" ============== word_in_progress")
    print("wordinprogress:",pc_word)
    lo_syllabble = Syllable.objects.get(word=pc_word)

    lc_examples_html = lo_syllabble.examples
    #print(lc_examples_html.replace(chr(13),'|').replace(chr(10), '*') )
    if lc_examples_html[-2:]!=chr(13)+chr(10):
        lc_examples_html = lc_examples_html + chr(13)+chr(10)
        if lc_examples_html[-2:] != chr(13) + chr(10):
            lc_examples_html = lc_examples_html + chr(13) + chr(10)

    paragraphs = lc_examples_html.split(chr(13)+chr(10)+chr(13)+chr(10))
    path_for_sounds = r'.\\vocapp\\static\\sounds\\examples\\'
    lc_quote = '"'
    lc_str = ''
    #DownLoadExamples(paragraphs)
    thr1 = threading.Thread(target=DownLoadExamples, args=(paragraphs,)).start()
    for part in paragraphs:
        lc_example = part.split('\n')
        if len(lc_example[0])>10:
            lc_file_name = load_syllable_from_wooordhunt.Delete_from_String_all_Characters_Unsuitable_For_FileName(lc_example[0])
            #lc_full_file_name = path_for_sounds + lc_file_name + '.mp3'
            #if not os.path.exists(lc_full_file_name):
            #    try:
            #        subprocess.run(["gtts-cli", lc_example[0], "--output", lc_full_file_name])
            #        print('saved:', lc_full_file_name)
            #    except:
            #        pass
            #lc_str = lc_str + "<p class = 'my_class_p_my_class_p_examples' onclick='new Audio( "+lc_quote+"/static/sounds/examples/" + lc_file_name + ".mp3"+lc_quote+" ).play(); return false;' >" + lc_example[0] + '</p>'
            lc_str = lc_str + "<p class = 'my_class_p_my_class_p_examples' >"+ lc_example[0]+\
                     "<IMG WIDTH='48' HEIGHT='48'  title = '' src='/static/images/audio.svg' onclick = '"+ \
                    'new Audio("/static/sounds/examples/' + lc_file_name + ".mp3" + '" ).play(); return false;'+\
                    "'>"  +'</p>'


        else:
            lc_str = lc_str + "<p class = 'my_class_p_my_class_p_examples' onclick='speakText(this.textContent)' >" + lc_example[0] + '</p>'
        if len(lc_example) >= 2:
            lc_str = lc_str + "<p  class = 'my_class_p_my_class_p_examples_russian' onclick='speakText(this.textContent)' >" + lc_example[1] + '</p> <br>'

    #lc_examples_html = add_format_for_russian(lc_str, 'my_class_p_my_class_p_examples_russian') #.replace(chr(13),'<br>')
    lc_examples_html = lc_str

    data = {    "word":lo_syllabble.word,
                "transcription":lo_syllabble.transcription,
                "translations":add_format_for_russian(lo_syllabble.translations, 'my_class_p_my_class_p_translations_russian').replace(chr(13),'<br>'),
                "examples":lc_examples_html, #add_format_for_russian(lo_syllabble.examples, 'my_class_p_my_class_p_examples_russian').replace(chr(13),'<br>')
                "number_of_words_to_study":str(len(Syllable.objects.filter(ready=0))),
                'number_of_words_learned':str(len(Syllable.objects.filter(ready=1))),
                "last_added_word":Syllable.objects.filter(ready=0).filter(show_count=0).order_by('-last_view')[0].word}
    return render(request, "word_in_progress.html", context=data)


def DownLoadmp3s (ll_sentences):
    path_for_sounds = r'.\\vocapp\\static\\sounds\\books\\'
    for sentence in ll_sentences:
        lc_sentence = sentence.strip()
        lc_file_name = hashlib.sha256(lc_sentence.encode('utf-8')).hexdigest() + '.mp3'
        lc_full_file_name = path_for_sounds + lc_file_name
        if not (os.path.exists(lc_full_file_name)) and len(lc_sentence) > 4:
            try:
                subprocess.run(["gtts-cli", lc_sentence, "--output", lc_full_file_name])
                print('saved:', lc_full_file_name)
            except:
                pass

def books(request):
    lo_book = Books.objects.filter()
    data = { 'books':lo_book }
    for book in lo_book:
        print(book.id_book, book.book_name, book.current_paragraph)
    return render(request, "books.html", context=data)

def book(request, pc_book:str, pc_paragraph:str):
    if int(pc_book)>0 and int(pc_paragraph)>0:
        path_for_sounds = r'.\\vocapp\\static\\sounds\\books\\'
        lo_book = Books.objects.get(id_book = int(pc_book))
        lo_book.current_paragraph = int(pc_paragraph)
        lo_book.save()

        lo_paragraph_navigation = Paragraphs.objects.filter(id_book=int(pc_book)).order_by('id_paragraph')[0]
        ln_start_id = lo_paragraph_navigation.id_paragraph
        lo_paragraph_navigation = Paragraphs.objects.filter(id_book=int(pc_book)).latest('id_paragraph')
        ln_end_id = lo_paragraph_navigation.id_paragraph

        lc_result_total = ''
        ln_alternation_counter = 0
        for i in range(-2,3):
            lc_result = ''
            if ln_start_id<=int(pc_paragraph)<=ln_end_id:
                lo_paragraph = Paragraphs.objects.get(id_book=int(pc_book), id_paragraph=int(pc_paragraph)+i)
                lc_source = lo_paragraph.paragraph
                sentences = re.split(r'(?<=[.!?…]) ', lc_source)
                #DownLoadmp3s(sentences)
                thr1 = threading.Thread(target=DownLoadmp3s, args=(sentences,)).start()
                for sentence in sentences:
                    ln_alternation_counter = ln_alternation_counter + 1
                    lc_sentence = sentence.strip()
                    print(ln_alternation_counter, lc_sentence)
                    lc_file_name = hashlib.sha256(lc_sentence.encode('utf-8')).hexdigest() + '.mp3'
                    if len(lc_sentence) > 2:
                        lc_result = lc_result + \
                                    ("<span class = 'my_class_p_my_class_p_books'>" if ln_alternation_counter%2==0 else "<span class = 'my_class_p_my_class_p_books_even'>") + lc_sentence + "</span>" + \
                                    ' &nbsp;&nbsp;&nbsp;' + \
                                    ("<IMG WIDTH='48' HEIGHT='48'  title = '' src='/static/images/audio.svg' onclick = '" + \
                                     'new Audio("/static/sounds/books/' + lc_file_name + '" ).play(); return false;' + \
                                     "'>" if len(lc_sentence.strip().replace('.', '')) > 3 else '') + chr(13)
            lc_result_total = lc_result_total + '<p class="my_class_p_my_class_p_examples">'+lc_result+'</p>' + chr(10) + '<br>'



        lc_link_on_start = "/book/" + pc_book + "/" + str(ln_start_id) +"/"
        lc_link_on_end   = "/book/" + pc_book + "/" + str(ln_end_id) + "/"

        lc_link_on_prev = "/book/" + pc_book + "/" + str(int(pc_paragraph)-5) + "/" if not(int(pc_paragraph)-5 < ln_start_id) else "/book/" + pc_book + "/" + str(ln_start_id) + "/"
        lc_link_on_next = "/book/" + pc_book + "/" + str(int(pc_paragraph)+5) +"/" if not(int(pc_paragraph)+5 > ln_end_id) else "/book/" + pc_book + "/" + str(ln_end_id) +"/"

        lc_in_book_position = str(int(pc_paragraph) - ln_start_id)+' / ' + str(ln_end_id - ln_start_id) + ' &nbsp;&nbsp;&nbsp;' + str(  round((int(pc_paragraph) - ln_start_id)*100 / (ln_end_id - ln_start_id),2))+' %'

        data = {"text": lc_result_total,
                'book_name':lo_book.book_name,
                'link_on_start':lc_link_on_start,
                'link_on_end':lc_link_on_end,
                'link_on_next':lc_link_on_next,
                'link_on_prev':lc_link_on_prev,
                'in_book_position':lc_in_book_position}
    else:
        data = {"text": '<p> Пример текста </p>'}
    return render(request, "book.html", context=data)




def next_with_last(request, pc_last_word):
    print(" ============== next_with_last")
    lo_sillable = Syllable.objects.get(word = pc_last_word)
    lo_sillable.show_count = lo_sillable.show_count + 1
    lo_sillable.last_view = datetime.datetime.now()
    lo_sillable.save()
    return redirect(next)

def next(request):
    print(" ============== next")
    lc_word =  Syllable.objects.filter(ready=0).order_by('last_view')[0].word
    print('===================')
    print("next:", lc_word)
    print('===================')
    return word_in_progress(request, lc_word)


def ready(request, pc_ready_word):
    print(" ============== ready")
    lo_sillable = Syllable.objects.get(word = pc_ready_word)
    lo_sillable.ready = 1
    lo_sillable.save()
    print('===================')
    print("ready:",pc_ready_word)
    print('===================')
    return redirect(index)


def unready(request, pc_unready_word):
    lo_sillable = Syllable.objects.get(word = pc_unready_word)
    lo_sillable.ready = 0
    lo_sillable.save()
    print('===================')
    print("unready:",pc_unready_word)
    print('===================')
    return redirect(ready_list)



from gtts import gTTS