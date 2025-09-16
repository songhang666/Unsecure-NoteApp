from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Note(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.FileField(upload_to='note_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shared_with = models.ManyToManyField(User, related_name='shared_notes', blank=True)
    is_public = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('note_detail', kwargs={'pk': self.pk})
    
    def get_share_url(self):
        return reverse('shared_note', kwargs={'pk': self.pk})

    @property
    def trimmed_title(self):
        if self.title:
            temp_title = self.title.replace(" ", "")
            return temp_title.title[:20] + '...' if len(temp_title) > 50 else temp_title
        return ''

class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.note.title}'