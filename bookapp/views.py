from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, BorrowForm, BookForm, DeleteBookForm,UserProfileUpdateForm
from .models import Book, Category, BorrowedBook
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User





# Create your views here.
def home(request):
    recommended_books = Book.objects.filter(recommended_books = True)
    fiction_books = Book.objects.filter(fiction_books = True)
    business_books = Book.objects.filter(business_books = True)
    return render(request, 'home.html', {'recommended_books': recommended_books,
    'business_books': business_books, 'fiction_books': fiction_books
    })


def all_books(request):
    books = Book.objects.all()
    return render(request, 'all_books.html', {'books':books})


def category_detail(request, slug):
    category = Category.objects.get(slug = slug)
    return render(request, 'category_detail.html', {'category': category})

@login_required(login_url='login')
def book_detail(request, slug):
    book = Book.objects.get(slug = slug)
    book_category = book.category.first()
    similar_books = Book.objects.filter(category__name__startswith = book_category)
    return render(request, 'book_detail.html', {'book': book, 'similar_books': similar_books})


def search_book(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('search_type', 'title')  # Default to 'title' if not specified
    category_query = request.GET.get('category', '')

    if search_type == 'author':
        base_query = Q(author__icontains=query)
    elif search_type == 'category':
        base_query = Q(category__name__icontains=query)
    else:  # Default to title search
        base_query = Q(title__icontains=query)

    if category_query:
        searched_books = Book.objects.filter(
            base_query,
            category__name__icontains=category_query
        ).distinct()
    else:
        searched_books = Book.objects.filter(base_query).distinct()

    return render(request, 'search_book.html', {'searched_books': searched_books})

def register_page(request):
    register_form = CreateUserForm()
    if request.method == 'POST':
        register_form = CreateUserForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.info(request, "Account Created Successfully!")
            return redirect('login')
           
    return render(request, 'register.html', {'register_form': register_form})

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  # Corrected from 'password1' to 'password'
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')  # Ensure you have a URL named 'admin_dashboard'
            else:
                return redirect('home')  # Ensure you have a URL named 'home'
        else:
            messages.info(request, "Invalid credentials")

    return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    return redirect('home')
  
    
@login_required
def borrow_book(request, slug):
    book = Book.objects.get(slug=slug)
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            borrow = form.save(commit=False)
            borrow.user = request.user
            borrow.book = book
            borrow.save()
            messages.success(request, "You have successfully borrowed the book.")
            return redirect('my_borrowed_books')
    else:
        form = BorrowForm()
    return render(request, 'borrow_book.html', {'form': form, 'book': book})

@login_required
def my_borrowed_books(request):
    borrowed_books = BorrowedBook.objects.filter(user=request.user)
    return render(request, 'my_borrowed_books.html', {'borrowed_books': borrowed_books})


@login_required
def return_book(request, pk):
    borrowed_book = get_object_or_404(BorrowedBook, pk=pk, user=request.user)
    if request.method == 'POST':
        borrowed_book.returned = True
        borrowed_book.save()
        messages.success(request, "You have successfully returned the book.")
        return redirect('my_borrowed_books')
    return render(request, 'my_borrowed_books.html', {'borrowed_book': borrowed_book})




def admin_dashboard(request):
    total_books = Book.objects.count()
    total_borrowed_books = BorrowedBook.objects.count()
    users = User.objects.count()  
    
    
    context = {
        'total_books': total_books,
        'total_borrowed_books': total_borrowed_books,
        'users': users,
    }

    return render(request, 'admin_dashboard.html', context)


    

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('admin_dashboard')  # Redirect to the admin dashboard
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})



def admin_all_books(request):
    books = Book.objects.all()
    return render(request, 'admin_all_books.html', {'books': books})

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form})

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = DeleteBookForm(request.POST)
        if form.is_valid():
            book.delete()
            return redirect('admin_dashboard')
    else:
        form = DeleteBookForm()
    return render(request, 'delete_book.html', {'form': form, 'book': book})


# from django.shortcuts import render
# from .models import Book

def admin_search_books(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('search_type', 'title')

    if search_type == 'title':
        books = Book.objects.filter(title__icontains=query)
    elif search_type == 'author':
        books = Book.objects.filter(author__icontains=query)
    elif search_type == 'category':
        books = Book.objects.filter(category__name__icontains=query)
    else:
        books = Book.objects.none()

    return render(request, 'admin_all_books.html', {'books': books})


#######################################################
@login_required
def update_profile(request):
    
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important: to keep the user logged in after password change
            return redirect('profile_updated')  # Redirect to a confirmation page or back to profile
    else:
        form = UserProfileUpdateForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})