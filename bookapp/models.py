from django.db import models    
from django.contrib.auth.models import User
# Create your models here.

class Category (models. Model):
    name = models.CharField('Categories', max_length=50)
    slug = models.SlugField(max_length = 50)
    def __str__(self):
        return self.name

class Book(models. Model):
    title = models. CharField(max_length = 100)
    slug = models.SlugField(max_length = 100)
    cover_image = models.ImageField(upload_to = 'img', blank = True, null = True)
    author = models.CharField(max_length=50)
    summary = models.TextField()
    category = models.ManyToManyField(Category, related_name='books', blank = True)
    pdf = models.FileField(upload_to='pdf', blank = True) 
    recommended_books = models.BooleanField(default=False)
    fiction_books = models.BooleanField(default=False)
    business_books = models.BooleanField(default=False)
    availability = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    
class BookSearch(models.Model):
    name_of_book = models.CharField(max_length=100)
    def __str__(self):
        return self.name_of_book

class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowed_by')
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"


