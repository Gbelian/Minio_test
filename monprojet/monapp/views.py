from django.shortcuts import render

from django.shortcuts import render
from .models import Resume, Post, Skill, Project, Category ,Paragraph,Citation

from .forms import CommentForm

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


def home(request):
    resumes = Resume.objects.all()
    posts = Post.objects.all()
    skills = Skill.objects.all()
    latest_posts = Post.objects.all().order_by('-published_at')[:3]
    projects = Project.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Send the email
            send_mail(
                subject,
                message,
                email,  # From email
                ['smtp.mailpro.com'],  # To email
                fail_silently=False,
            )
            messages.success(request, 'Message sent successfully.')
            return redirect('home')
    else:
        form = ContactForm()

    context = {
        'categories': categories,
        'resumes': resumes,
        'posts': latest_posts,
        'skills': skills,
        'projects': projects,
        'form': form,
    }

    return render(request, 'monapp/index.html', context)


from django.shortcuts import render, get_object_or_404
from .models import Post



from django.shortcuts import render, get_object_or_404
from .models import Post, Category

from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, Category
from .forms import CommentForm

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse



from django.shortcuts import render
from .models import Post


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    citations = Citation.objects.all()
    paragraphs = Paragraph.objects.all()
    recent_posts = Post.objects.all().order_by('-published_at')[:3]
    categories = Category.objects.all()
    comments = Comment.objects.all()
    comment = post.comments.filter(active=True, parent__isnull=True)
    new_comment = None
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_id = request.POST.get('parent_id')
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            if parent_id:
                new_comment.parent = Comment.objects.get(id=parent_id)
            new_comment.photo = request.FILES['photo']
            new_comment.save()
            comment_form = CommentForm()
            return HttpResponseRedirect(reverse('post_detail', args=[slug]))
        else:
            query = request.GET.get('q')
            results = Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query)
            post = results
    
    
    return render(request, 'monapp/single.html', {
        'post': post,
        'paragraphs' : paragraphs,
        'citations': citations,
        'categories': categories,
        'recent_posts': recent_posts,
        'comments': comment,
        'new_comment': new_comment,
        'comment_form': comment_form,
    })




