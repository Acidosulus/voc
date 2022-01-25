"""voc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vocapp import views

urlpatterns = [
	path('', views.index),
	path('test', views.test),
	path('test/', views.test),
	path('admin', admin.site.urls),
	path('word_in_progress/<str:pc_word>/', views.word_in_progress),
	path('add_new/<str:pc_new_word>/', views.add_new_with_parameter),
	path('add_new', views.add_new),
	path('add_new/', views.add_new),
	path('ready_list/', views.ready_list),
	path('next/<str:pc_last_word>/', views.next_with_last),
	path('next/', views.next),
	path('ready/<str:pc_ready_word>/', views.ready),
	path('unready/<str:pc_unready_word>/', views.unready),
	path('book/<str:pc_book>/<str:pc_paragraph>/', views.book),
	path('books/', views.books),

]

