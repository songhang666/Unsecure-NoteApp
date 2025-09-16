from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

from notes import views

urlpatterns = [
    path('', include('notes.urls')),
    path(settings.ADMIN_MAGIC, admin.site.urls),
    path('auth/', include('myauth.urls')),
    
    # technical URLs
    path('debug/settings/', views.debug_settings, name='debug_settings'),
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
]