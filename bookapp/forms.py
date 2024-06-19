from django import forms
from .models import BookSearch, BorrowedBook, Book, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404



class BookSearchForm(forms.ModelForm):
    name_of_book = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': "form-control", 'placeholder': 'Search Book'
    }))
    class Meta:
        model = BookSearch
        fields = ['name_of_book',]

class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter Username'
    }))
    email = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter Email Address'
    }))
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'At least eight characters'
    }))
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm Password'
    }))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BorrowForm(forms.ModelForm):
    class Meta:
        model = BorrowedBook
        fields = ['return_date']
        widgets = {
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AdminProfileUpdateForm(UserChangeForm):
    email = forms.EmailField(required=True, label='New Email')
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput, help_text='')
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput, help_text='')

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        return self.cleaned_data['email']

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if self.cleaned_data['new_password1']:
            user.set_password(self.cleaned_data['new_password1'])
        if commit:
            user.save()
        return user

class BookForm(forms.ModelForm):
    new_category = forms.CharField(max_length=100, required=False, help_text="Or add a new category")

    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].required = False

    def save(self, commit=True):
        instance = super(BookForm, self).save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        new_category_name = self.cleaned_data.get('new_category')
        if new_category_name:
            category, created = Category.objects.get_or_create(name=new_category_name)
            instance.category.add(category)
        return instance

class DeleteBookForm(forms.Form):
    pass

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff', 'is_active']

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'is_active']
        
        ################################################
        
class UserProfileUpdateForm(UserChangeForm):
    email = forms.EmailField(required=True, label='Email')
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput, required=False, help_text='')
    password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput, required=False, help_text='')
    
    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
    
    
    
    
class AdminProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = AdminProfileUpdateForm
    template_name = 'admin_profile.html'

    def get_object(self):
        # Ensure the user can only update their own profile
        return self.request.user

    def form_valid(self, form):
        # Save the form and update the session auth hash if password was changed
        user = form.save()
        update_session_auth_hash(self.request, user)  # This will update the session hash if the password was changed
        return super().form_valid(form)
    
    
    
    


class UsersListView(ListView):
    model = User
    template_name = 'users_list.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('all_users')

class UserEditView(UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'user_form.html'
    success_url = reverse_lazy('all_users')

class UserDeleteView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        messages.success(request, 'User has been deleted.')
        return redirect('all_users')
