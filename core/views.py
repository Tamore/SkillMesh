from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import models
from .services import register_user, update_profile, add_skill_to_user, create_post, send_message, search_users_by_skill
from .forms import ProfileForm, SkillForm, PostForm, MessageForm, CustomUserCreationForm, UserUpdateForm
from .models import Post, Message, UserProfile, Event
import time

def index(request):
    """Simple home page / feed."""
    posts = Post.objects.all().order_by('-created_at')
    user_count = User.objects.count()
    post_count = Post.objects.count()
    return render(request, 'core/index.html', {
        'posts': posts,
        'user_count': user_count,
        'post_count': post_count
    })

from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Generate username from full name
            full_name = form.cleaned_data.get('full_name')
            username = full_name.replace(" ", "").lower()
            
            # Ensure uniqueness
            if User.objects.filter(username=username).exists():
                username = f"{username}{User.objects.count()}"
                
            try:
                user = register_user(
                    username=username,
                    email=form.cleaned_data.get('email'),
                    password=form.cleaned_data.get('password'),
                    bio=f"Hi, I'm {full_name}."
                )
            except Exception as e:
                messages.error(request, "REGISTRATION FAILED. PROTOCOL SYNCHRONIZATION ERROR.")
                return render(request, 'core/register.html', {
                    'form': form,
                    'user_count': User.objects.count(),
                    'post_count': Post.objects.count()
                })
            login(request, user)
            messages.success(request, f"Welcome to the mesh, {username}! Your protocol has been initialized.")
            return redirect('index')
        else:
            messages.error(request, "Registration failed. Please check your inputs.")
    else:
        form = CustomUserCreationForm()
    
    user_count = User.objects.count()
    post_count = Post.objects.count()
    return render(request, 'core/register.html', {
        'form': form,
        'user_count': user_count,
        'post_count': post_count
    })

def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try standard authentication first
        user = authenticate(request, username=username_or_email, password=password)
        
        # If that fails, try email authentication
        if user is None and '@' in username_or_email:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Access granted. Welcome back, {user.username}.")
            next_url = request.POST.get('next') or request.GET.get('next')
            if not next_url or next_url == 'None' or 'login' in next_url:
                next_url = 'index'
            return redirect(next_url)
        else:
            messages.error(request, "Authentication failed. Invalid identifier or cipher.")
            # Fallback to form for error display
            form = AuthenticationForm(request, data=request.POST)
            return render(request, 'core/login.html', {'form': form})
    else:
        form = AuthenticationForm()
    
    user_count = User.objects.count()
    post_count = Post.objects.count()
    return render(request, 'core/login.html', {
        'form': form,
        'user_count': user_count,
        'post_count': post_count
    })

def logout_view(request):
    logout(request)
    messages.info(request, "Session terminated. Your protocol has been de-indexed.")
    return redirect('index')

@login_required
def profile_view(request):
    """View a user's profile. Defaults to the logged-in user."""
    username = request.GET.get('username')
    if username:
        try:
            user_to_view = User.objects.get(username=username)
            profile, _ = UserProfile.objects.get_or_create(user=user_to_view)
        except User.DoesNotExist:
            messages.error(request, "Identity not found in the mesh.")
            return redirect('index')
    else:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'core/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    """Edit user profile (bio, picture, etc), change username and password."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile_form = ProfileForm(instance=profile)
    user_form = UserUpdateForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
            user_form = UserUpdateForm(request.POST, instance=request.user)
            if profile_form.is_valid() and user_form.is_valid():
                user_form.save()
                update_profile(
                    user=request.user,
                    bio=profile_form.cleaned_data.get('bio'),
                    profile_picture=request.FILES.get('profile_picture'),
                    open_to_work=profile_form.cleaned_data.get('open_to_work')
                )
                messages.success(request, "Identity and profile updated successfully.")
                return redirect('profile')
                
        elif action == 'change_password':
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, "Password successfully rotated.")
                return redirect('profile')
            else:
                messages.error(request, "Password update failed. Please verify the protocol requirements.")

    return render(request, 'core/edit_profile.html', {
        'form': profile_form,
        'user_form': user_form,
        'password_form': password_form,
        'profile': profile
    })



@login_required
def add_skill(request):
    """Add a skill to the user's profile."""
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            add_skill_to_user(request.user, form.cleaned_data.get('skill_name'))
            return redirect('profile')
    return redirect('profile')

@login_required
def create_post_view(request):
    """Create a new post."""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            create_post(
                user=request.user,
                content=form.cleaned_data.get('content'),
                post_type=form.cleaned_data.get('post_type'),
                skill_ids=form.cleaned_data.get('related_skills')
            )
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'core/create_post.html', {'form': form, 'title': 'Broadcast Signal'})

@login_required
def edit_post_view(request, post_id):
    """Edit an existing post."""
    post = Post.objects.get(id=post_id)
    if post.user != request.user:
        messages.error(request, "Unauthorized protocol access.")
        return redirect('index')
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Signal updated successfully.")
            return redirect('index')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'core/create_post.html', {'form': form, 'title': 'Recalibrate Signal', 'edit_mode': True})

@login_required
def delete_post_view(request, post_id):
    """Delete a post."""
    post = Post.objects.get(id=post_id)
    if post.user == request.user:
        post.delete()
        messages.success(request, "Signal terminated.")
    else:
        messages.error(request, "Unauthorized protocol termination.")
    return redirect('index')

@login_required
def inbox_view(request):
    """View conversations."""
    # Get all unique users the current user has messaged or received messages from
    sent_to = Message.objects.filter(sender=request.user).values_list('receiver', flat=True)
    received_from = Message.objects.filter(receiver=request.user).values_list('sender', flat=True)
    user_ids = set(list(sent_to) + list(received_from))
    
    conversations = []
    for user_id in user_ids:
        peer = User.objects.get(id=user_id)
        last_msg = Message.objects.filter(
            (models.Q(sender=request.user) & models.Q(receiver=peer)) |
            (models.Q(sender=peer) & models.Q(receiver=request.user))
        ).order_by('-timestamp').first()
        conversations.append({
            'peer': peer,
            'last_message': last_msg
        })
    
    # Sort conversations by last message timestamp
    conversations.sort(key=lambda x: x['last_message'].timestamp, reverse=True)

    return render(request, 'core/inbox.html', {
        'conversations': conversations
    })

@login_required
def send_message_view(request, username):
    """View conversation history and send a message."""
    receiver = User.objects.get(username=username)
    history = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=receiver)) |
        (models.Q(sender=receiver) & models.Q(receiver=request.user))
    ).order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            send_message(
                sender=request.user,
                receiver_username=username,
                content=form.cleaned_data.get('content')
            )
            return redirect('send_message', username=username)
    else:
        form = MessageForm()
    
    return render(request, 'core/send_message.html', {
        'form': form, 
        'receiver': receiver,
        'history': history
    })


def search_view(request):
    """Search for users by skill."""
    query = request.GET.get('q', '')
    results = search_users_by_skill(query)
    return render(request, 'core/search_results.html', {'results': results, 'query': query})

def opportunities_view(request):
    """View and search for 'hiring' posts."""
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(
            models.Q(post_type='hiring') & 
            (models.Q(content__icontains=query) | models.Q(related_skills__name__icontains=query))
        ).distinct().order_by('-created_at')
    else:
        posts = Post.objects.filter(post_type='hiring').order_by('-created_at')
    
    return render(request, 'core/opportunities.html', {'posts': posts, 'query': query})

import csv
from django.http import HttpResponse

@login_required
def insights_view(request):
    """Founder Dashboard to view system event statistics."""
    if not request.user.is_staff:
        messages.error(request, "Access Denied: Founder credentials required for protocol insights.")
        return redirect('index')
    
    events = Event.objects.all().order_by('-timestamp')
    total_events = events.count()
    success_count = events.filter(status='success').count()
    failure_count = events.filter(status='failure').count()
    avg_time = events.aggregate(models.Avg('processing_time'))['processing_time__avg'] or 0
    
    return render(request, 'core/insights.html', {
        'events': events[:50], # Show last 50 events
        'total_events': total_events,
        'success_count': success_count,
        'failure_count': failure_count,
        'avg_time': round(avg_time, 2)
    })

@login_required
def export_events_csv(request):
    """Export all events to a CSV file for research and auditing."""
    if not request.user.is_staff:
        return HttpResponse("Unauthorized protocol access.", status=401)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="skillmesh_system_events.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Event Type', 'Timestamp', 'Processing Time (ms)', 'Status'])
    
    events = Event.objects.all().order_by('-timestamp')
    for event in events:
        writer.writerow([event.event_type, event.timestamp, event.processing_time, event.status])
        
    return response
