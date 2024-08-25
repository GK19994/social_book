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