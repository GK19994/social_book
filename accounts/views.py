from django.shortcuts import render, HttpResponseRedirect,redirect
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
import django_filters
from .models import UploadedFile
from .forms import UploadFileForm
import pandas as pd
import numpy as np

# Create your views here.


def sign_up(request):
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request,'Account  Created Successfully')
            fm.save()
    else:
        fm = SignUpForm()
    return render(request,'accounts/signup.html',{'form':fm})



def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Logged in successfully !!")
                    return HttpResponseRedirect('/accounts/profile/')

        else:
            fm =  AuthenticationForm()
        return render(request,'accounts/userlogin.html',{'form': fm})
    else:
        return HttpResponseRedirect('/accounts/profile/')

def user_profile(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/profile.html' ,{'name':request.user}) 
    else:
        return HttpResponseRedirect('/accounts/userlogin')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/accounts/userlogin')



# Custom filter for CustomUser model
class CustomUserFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = ['public_visibility']

@login_required
def authors_and_sellers(request):
    user_filter = CustomUserFilter(request.GET, queryset=CustomUser.objects.filter(public_visibility=True,is_superuser=False))
    return render(request, 'accounts/authors_and_sellers.html', {'users': user_filter.qs})



@login_required
def upload_books(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('upload_books')
    else:
        form = UploadFileForm()
    return render(request, 'accounts/upload_books.html', {'form': form})

@login_required
def uploaded_files(request):
    files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'accounts/uploaded_files.html', {'files': files})


def data_wrangling_view(request):
    #Create a pandas DataFrame (size: 10x3) from a list of values/dictionary
    data = {
        'Author': ['Author1', 'Author2', 'Author3', 'Author4', 'Author5', 
                   'Author6', 'Author7', 'Author8', 'Author9', 'Author10'],
        'Book Title': ['Book1', 'Book2', 'Book3', 'Book4', 'Book5', 
                       'Book6', 'Book7', 'Book8', 'Book9', 'Book10'],
        'Year Published': [2001, 2003, 1999, 2015, 2020, 1987, 1995, 2010, 2008, 2022]
    }
    df = pd.DataFrame(data)

    #Filter DataFrame based on a Year Published greater than 2000 and print
    filtered_df = df[df['Year Published'] > 2000]

    #Filter DataFrame with columns 'Author' and 'Book Title' and print
    filtered_columns_df = df[['Author', 'Book Title']]

    #Replace Year Published with 'Modern' if after 2000, else 'Classic'
    df['Year Category'] = df['Year Published'].apply(lambda x: 'Modern' if x > 2000 else 'Classic')

    #Create another DataFrame and append it to the original one
    additional_data = {
        'Author': ['Author11', 'Author12'],
        'Book Title': ['Book11', 'Book12'],
        'Year Published': [1990, 2021]
    }
    df2 = pd.DataFrame(additional_data)
    appended_df = pd.concat([df, df2], ignore_index=True)

    # Passing data to the template
    context = {
        'original_df': df.to_html(index=False),
        'filtered_df': filtered_df.to_html(index=False),
        'filtered_columns_df': filtered_columns_df.to_html(index=False),
        'replaced_df': df.to_html(index=False),
        'appended_df': appended_df.to_html(index=False),
    }

    return render(request, 'accounts/data_wrangling.html', context)
