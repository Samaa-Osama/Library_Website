from django.contrib import admin
from .models import Category, Book, BookSearch


from .models import BorrowedBook
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
    
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookSearch)
# admin.site.register(BorrowedBook)

class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'borrow_date', 'return_date', 'returned')

admin.site.register(BorrowedBook, BorrowedBookAdmin)