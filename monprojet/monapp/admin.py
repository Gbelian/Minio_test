from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Resume, Skill, Project, Category, Post, Comment, Citation, Paragraph

class CustomAdminSite(AdminSite):
    site_header = 'Portefolio'
    site_title = 'Admin'
    index_title = 'Tableau de bord'

custom_admin_site = CustomAdminSite(name='customadmin')

# Définir la classe d'administration pour le modèle Resume
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('diplome', 'date_debut', 'date_fin')
    list_filter = ('date_debut', 'date_fin')
    search_fields = ('diplome',)

# Définir la classe d'administration pour le modèle Skill
class SkillAdmin(admin.ModelAdmin):
    list_display = ('titre', 'pourcentage')

class CitationAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'content')

class ParagraphAdmin(admin.ModelAdmin):
    list_display = ('titre', 'content')

# Définir la classe d'administration pour le modèle Project
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('titre', 'description', 'domaine')  # Ajout de 'description'
    search_fields = ('titre', 'description')  # Ajout de 'description'

# Définir la classe d'administration pour le modèle Category
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# Définir la classe d'administration pour le modèle Post
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at', 'published_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

# Définir la classe d'administration pour le modèle Comment
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'active')
    list_filter = ('created_at', 'active')
    search_fields = ('author', 'content')



# Importez vos classes d'administration personnalisées
from .admin import ResumeAdmin, SkillAdmin, ProjectAdmin, CategoryAdmin, PostAdmin, CommentAdmin ,CitationAdmin ,ParagraphAdmin

# Inscrivez vos classes d'administration personnalisées sur votre site d'administration personnalisé
custom_admin_site = CustomAdminSite()

custom_admin_site.register(Resume, ResumeAdmin)

custom_admin_site.register(Citation, CitationAdmin)
custom_admin_site.register(Paragraph, ParagraphAdmin)

custom_admin_site.register(Skill, SkillAdmin)
custom_admin_site.register(Project, ProjectAdmin)
custom_admin_site.register(Category, CategoryAdmin)
custom_admin_site.register(Post, PostAdmin)
custom_admin_site.register(Comment, CommentAdmin)
