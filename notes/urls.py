from django.urls import include, path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    
    # Note URLs
    path('', views.splash, name='splash'),
    path('mynotes/', views.note_list_view, name='note_list'),
    path('create/', views.note_create_view, name='note_create'),
    path('note/<int:pk>/', views.note_detail_view, name='note_detail'),
    path('note/<int:pk>/edit/', views.note_edit_view, name='note_edit'),
    path('note/<int:pk>/delete/', views.note_delete_view, name='note_delete'),
    path('search/', views.note_search_view, name='note_search'),
    path('get_random_photo/', views.get_random_photo, name='get_random_photo'),
    
    # Shared note URL
    path('shared/<int:pk>/', views.shared_note_view, name='shared_note'),
]

