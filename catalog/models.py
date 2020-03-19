from django.db import models
from django.urls import reverse
from datetime import date
import uuid


# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Введите название жанра", verbose_name="Жанр")

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Введите исходный язык книги", verbose_name="Язык")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=300, help_text="Введите название книги", verbose_name="Название Книги")
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, help_text="Автор",
                               verbose_name="Авторы Книги")
    summary = models.TextField(max_length=1000, help_text="Введите описание книги", verbose_name="Описание книги")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 значный Международный стандартный книжный номер  <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>"')
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр для книги")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Жанры'

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Уникальный ID книги внутри библиотеки", verbose_name="Уникальный ID")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, verbose_name="Наменование Книги")
    imprint = models.CharField(max_length=200, verbose_name="Издательство")
    due_back = models.DateField(null=True, blank=True, verbose_name="Дата появления")

    LOAN_STATUS = (
        ('m', 'Ожидается поступление'),
        ('o', 'Выдан'),
        ('a', 'Доступна'),
        ('r', 'Зарезервирована'),
        ('n', 'Недоступна')
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m',
                              help_text='Доступность Книги')

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return ' %s ' % (self.book.title)


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя Автора")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия Автора")
    date_of_birth = models.DateField('Рожден',null=True, blank=True)
    date_of_death = models.DateField('Умервщлен', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)
