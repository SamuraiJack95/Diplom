from django.shortcuts import render, redirect
from .models import Profile, User, Message
from django.contrib.auth import logout, login, authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForms, MessageForm
from django.contrib.auth.decorators import login_required
from .utils import search_profiles

def login_user(request):
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request, 'User with this username does not exists')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'users/login_register.html')

def logout_user(request):
    logout(request)
    messages.error(request, 'User was logged out')
    return redirect('login')

def profiles(request):
    prof, search_query = search_profiles(request)

    context = {'profiles': prof, 'search_query': search_query}
    return render(request, 'users/articles.html', context)

def user_profile(request, pk):
    prof = Profile.objects.get(id=pk)
    context = {'profile': prof}
    return render(request, 'users/profile.html', context)

def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'An error has occurred during registration!')
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)

@login_required(login_url='login')
def user_account(request):
    prof = request.user.profile
    articles = prof.article_set.all()
    context = {
        'profile': prof,
        'articles': articles,
    }
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForms(instance=profile)

    if request.method == 'POST':
        form = ProfileForms(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('user_account')
    context = {'form': form}
    return render(request, 'users/profile-form.html', context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messages_request = profile.messages.all()
    unread_count = messages_request.filter(is_read=False).count()

    context = {'messages_request': messages_request, 'unread_count': unread_count}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read is False:
        message.is_read = True
        message.save()

    context = {'message': message}
    return render(request, 'users/message.html', context)

def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    if request.user.is_authenticated and request.user.profile.id == recipient.id:
        messages.error(request, "You can't send message to yourself")
        return redirect('user_profile', pk=pk)
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form .save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            messages.success(request, 'Your message send successfully!')
            message.save()

            return redirect('user_profile', pk=recipient.id)

    context = {
        'recipient': recipient,
        'form': form
    }
    return render(request, 'users/message_form.html', context)