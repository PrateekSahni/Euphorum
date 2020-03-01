from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import NewTopicForm, RegisterForm, PostForm
from .models import Category, Topic, Post
from django.http import Http404
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from paralleldots import set_api_key, get_api_key, emotion
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


from .emotion import get_emotion
from .summarizer import get_summary
from .models import Category

def mood(request):
    return render(request, 'homepage/emotion.html' , )

def detect_emotion(request):
    result = get_emotion( (request.GET.get('mytext')))
    #return render(request,'homepage/emotion.html',{'result':result})
    return render(request, 'homepage/emotion.html', {'result': result})


def summarize(request):
    return render(request,'homepage/summarize.html')

def display_summary(request):
    summary = get_summary((request.GET.get('text')))
    return render(request,'homepage/summarize.html',{'summary':summary})


def index(request):
    categories = Category.objects.all()
    return render(request, 'homepage/index.html', {'categories': categories})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, user)
            #return render(request, 'homepage/index.html')
            return redirect('homepage:index')

    else:
        form = RegisterForm()
    return render(request, 'homepage/register.html', {'form': form})



def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return render(request, 'homepage/index.html')
            else:
                return render(request, 'homepage/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'homepage/login.html', {'error_message': 'Invalid login'})
    return render(request, 'homepage/login.html')


# def signout(request):
#     logout(request)
#     return redirect('homepage/index')


def category_topics(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'homepage/topics.html', {'category': category})

@login_required
def new_topic(request, pk):
    category = get_object_or_404(Category, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.category = category
            topic.creator = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )

            return redirect('homepage:topic_posts', pk=pk, topic_pk=topic.pk)
           # return category_topics(request, category.pk)
           # return render(request,'homepage/category_topics.html', pk=category.pk)
            #return redirect('homepage/category_topics', pk=category.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'homepage/new_topic.html', {'category': category, 'form': form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, category_id=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'homepage/topic_posts.html', {'topic': topic})


@login_required
def new_post(request, pk, topic_pk):
    topic = get_object_or_404(Topic, category_id=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('homepage:topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'homepage/new_post.html', {'topic': topic, 'form': form})
