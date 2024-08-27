from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from .api_views import UserFilesView


urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('userlogin/', views.user_login, name='userlogin'),
    path('profile/', views.user_profile, name='profile'),
    path('logout/', views.user_logout, name='log_out'),
    path('authors_sellers/', views.authors_and_sellers, name='authors_and_sellers'),
    path('upload-books/', views.upload_books, name='upload_books'),
    path('uploaded-files/', views.uploaded_files, name='uploaded_files'),
    path('data-wrangling/', views.data_wrangling_view, name='data_wrangling'),
    path('api/files/', UserFilesView.as_view(), name='user-files'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

]
