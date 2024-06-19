from django.urls import path
from . import views
from .forms import AdminProfileUpdateView

from .forms import UsersListView, UserCreateView, UserEditView, UserDeleteView


urlpatterns = [
    path('home', views.home, name= 'home'),
    path('all_books', views.all_books, name = 'all_books'),
    path('category/<str:slug>', views.category_detail, name='category_detail'),
    path('<str:slug>', views.book_detail, name='book_detail'),
    path('searched_books/', views.search_book, name = 'book_search'),
    
    path('register/', views.register_page, name = 'register'),
    path('login/', views.login_page, name = 'login'),
    path('logout/', views.logout_user, name = 'logout'),
    
    path('borrow/<slug:slug>/', views.borrow_book, name='borrow_book'),
    path('my_borrowed_books/', views.my_borrowed_books, name='my_borrowed_books'),
    
    path('return_book/<int:pk>/', views.return_book, name='return_book'),
    
    
    
    path('builtadmin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('builtadmin/profile/', AdminProfileUpdateView.as_view(), name='admin_profile'),
    
    path('builtadmin/add_book/', views.add_book, name='add_book'),
    
    path('builtadmin/admin_all_books/', views.admin_all_books, name='admin_all_books'),
    path('builtadmin/edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('builtadmin/delete_book/<int:pk>/', views.delete_book, name='delete_book'),
    path('builtadmin/admin_search_books/', views.admin_search_books, name='admin_search_books'),
    path('builtadmin/users/', UsersListView.as_view(), name='all_users'),
    path('builtadmin/users/add/', UserCreateView.as_view(), name='add_user'),
    path('builtadmin/users/edit/<int:pk>/', UserEditView.as_view(), name='edit_user'),
    path('builtadmin/users/delete/<int:pk>/', UserDeleteView.as_view(), name='delete_user'),
    
    path('updateuserprofile/', views.update_profile, name='update_profile'),
    
]
