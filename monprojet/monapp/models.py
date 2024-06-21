from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

class Resume(models.Model):
    diplome = models.CharField(max_length=200)
    universite = models.TextField()
    description = models.TextField()
    date_debut = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.diplome
    
class Citation(models.Model):
    auteur = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='citation_images/')  
    
    def __str__(self):
        return self.auteur



class Paragraph(models.Model):
    titre = models.CharField(max_length=200)
    content = models.TextField()
    def __str__(self):
        return self.titre

class Skill(models.Model):
    titre = models.CharField(max_length=100)  # Correction: Ajout de max_length
    pourcentage = models.IntegerField()
    
    def __str__(self):
        return self.titre
    
from django.db import models

class Project(models.Model):
    titre = models.CharField(max_length=200)  # Définition du type de champ
    description = models.TextField()  # Définition du type de champ
    image = models.ImageField(upload_to='project_images/')  # Définition du type de champ
    domaine = models.CharField(max_length=100)  # Définition du type de champ
    lien = models.URLField(max_length=200, default='http://example.com')  # Définir une valeur par défaut

    def __str__(self):
        return self.titre


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_posts', kwargs={'slug': self.slug})


class Post(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='post_images/')  # Correction: Définition du type de champ
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    content1 = models.TextField(default='Default content1 text')
    description = models.TextField(default='Default description text')
    paragraph2 = models.TextField(default='Default description text')
    paragraph3 = models.TextField(default='Default description text')
    paragraph4 = models.TextField(default='Default description text')
    created_at = models.DateTimeField(default=timezone.now)
    published_at = models.DateTimeField(blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='auteur_images/', default='auteur_images/staff-1.jpg')
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)


    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
 