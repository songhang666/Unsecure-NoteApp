import os, hashlib, logging, urllib, json

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db import connection

from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from noteapp import settings as SETTINGS
from .models import Note
from .forms import NoteForm, CommentForm

logger = logging.getLogger(__name__)

def splash(request):
    """Render the splash page with links to register and login."""
    logger.info("Rendering splash page")
    if request.user.is_authenticated:
        return redirect('note_list')
    return render(request, 'notes/splash.html', {'title': 'Welcome to Unsecure Notes App'})

@login_required
def note_list_view(request):
    """Render the list of all my notes."""
    logger.info("Rendering note list for user: %s", request.user.username)
    notes = Note.objects.filter(author=request.user)
    return render(request, 'notes/note_list.html', {
        'notes': notes,
        'title': 'My Notes'
    })

@login_required
def note_create_view(request):
    """Render the form to create a new note."""
    logger.info("Rendering note creation form for user: %s with request type: %s", request.user.username, request.method)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            messages.success(request, 'Note created successfully!')
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {
        'form': form,
        'title': 'Create Note',
        'button_text': 'Create Note'
    })

@login_required
def note_detail_view(request, pk):
    """Render the detail view of a note with comments. Also handles comment submission."""
    logger.info("Rendering note detail for note ID: %s", pk)
    note = get_object_or_404(Note, pk=pk, author=request.user)
    comments = note.comments.all()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.note = note
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('note_detail', pk=pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'notes/note_detail.html', {
        'note': note,
        'comments': comments,
        'comment_form': comment_form,
        'title': note.title
    })

@login_required
def note_edit_view(request, pk):
    """Render the form to edit an existing note."""
    logger.info("Rendering note edit form for note ID: %s", pk)
    #Andrew V7
    note = get_object_or_404(Note, pk=pk, author=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully!')
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)
    
    return render(request, 'notes/note_form.html', {
        'form': form,
        'note': note,
        'title': 'Edit Note',
        'button_text': 'Update Note'
    })

@login_required
def note_delete_view(request, pk):
    """Render the confirmation page to delete a note and handle note deletion."""
    logger.info("Rendering note delete confirmation for note ID: %s", pk)
    note = get_object_or_404(Note, pk=pk, author=request.user)
    
    if request.method == 'POST':
        note.delete()
        logger.info("Note ID: %s deleted by user: %s", pk, request.user.username)
        messages.success(request, 'Note deleted successfully!')
        return redirect('note_list')
    
    return render(request, 'notes/note_confirm_delete.html', {
        'note': note,
        'title': 'Delete Note'
    })

def shared_note_view(request, pk):
    """Render a shared note view with comments. Only public notes can be accessed."""
    logger.info("Rendering shared note view for note ID: %s", pk)
    note = get_object_or_404(Note, pk=pk, is_public=True)
    comments = note.comments.all()
    
    comment_form = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                logger.info("Adding comment to shared note ID: %s by user: %s", pk, request.user.username)
                comment = comment_form.save(commit=False)
                comment.note = note
                comment.author = request.user
                comment.save()
                messages.success(request, 'Comment added successfully!')
                return redirect('shared_note', pk=pk)
        else:
            comment_form = CommentForm()
    
    return render(request, 'notes/shared_note.html', {
        'note': note,
        'comments': comments,
        'comment_form': comment_form,
        'title': f'Shared: {note.title}'
    })

@login_required
def note_search_view(request):
    """Search for notes by title. Show all public notes that match the search query."""
    if request.method == 'GET':
        # don't ask why 'q' is used, it's just a common convention
        query = request.GET.get('q', '').strip()
            
        notes = Note.objects.filter(is_public=True)

        if query:
            notes = notes.filter(title__icontains=query)

        logger.info("Search query run", extra={
            "user_id": getattr(request.user, "id", None),
            "query": query,
            "results_count": len(notes),
        })

        # append author info
        notes = notes.select_related('author')
        # filter columns
        notes = notes.only(
            "id", "title", "author__username", "author__email",
            "created_at", "is_public", "content", "image"
        )

        return render(
            request,
            'notes/note_search.html',
            {
                'notes': notes,
                'query': query,
                'title': 'Search Results',
            }
        )
    else:
        raise Http404

def get_random_photo(request):
    """Get a random photo from BoringAPI."""
    if request.method == "GET":
        logger.info(f"Get a Random Photo from {request.GET["api_url"]}")
        try:
            with urllib.request.urlopen(request.GET["api_url"]) as response:
                response = response.read().decode()
                logger.info(f"Response from API: {response}")
                return HttpResponse(response)
        except Exception:
            logger.exception("Can't load " + request.GET['api_url'])
            return HttpResponse("Error loading photo", status=500)

    raise Http404

def debug_settings(request):
    if "X-Admin-Magic" in request.headers and hashlib.md5(request.headers["X-Admin-Magic"].encode()).hexdigest() == SETTINGS.DEBUG_MAGIC:
        with open(os.path.join(SETTINGS.BASE_DIR, 'noteapp/settings.py'), "r") as f:
            content = f.read()
        response = HttpResponse(content, "text/plain")
        return response
    
    logger.warning(f"Invalid headers {request.headers}")
    response = render(request, "403.html")
    response["X-Admin-Magic"] = "Invalid header!"
    return response
