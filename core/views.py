import os
import json
import csv
from django.db.models.functions import TruncDay
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import models
from django.core.paginator import Paginator
from django.db.models.functions import TruncDay
from django.http import HttpResponse, JsonResponse
from .services import register_user, update_profile, add_skill_to_user, create_post, send_message, search_users_by_skill
from .forms import ProfileForm, SkillForm, PostForm, MessageForm, CustomUserCreationForm, UserUpdateForm
from .models import Post, Message, UserProfile, Event, Comment, SavedPost
import time

def index(request):
    """Simple home page / feed."""
    posts = Post.objects.all().order_by('-created_at')
    user_count = User.objects.count()
    post_count = Post.objects.count()
    saved_post_ids = []
    if request.user.is_authenticated:
        # Ensure profile exists to prevent crashes
        UserProfile.objects.get_or_create(user=request.user)
        saved_post_ids = SavedPost.objects.filter(user=request.user).values_list('post_id', flat=True)

    return render(request, 'core/index.html', {
        'posts': posts,
        'user_count': user_count,
        'post_count': post_count,
        'saved_post_ids': saved_post_ids
    })

@login_required
def insights_view(request):
    if not request.user.is_staff:
        return redirect('index')
    
    # Aggregated Chart Data
    chart_data = Event.objects.annotate(day=TruncDay('timestamp')).values('day').annotate(count=models.Count('id')).order_by('day')
    chart_labels = [d['day'].strftime('%b %d') for d in chart_data]
    chart_values = [d['count'] for d in chart_data]

    # Paginated Event Table
    event_list = Event.objects.all().order_by('-timestamp')
    paginator = Paginator(event_list, 15) # 15 entries per page
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)

    avg_time = Event.objects.aggregate(models.Avg('processing_time'))['processing_time__avg'] or 0
    total_events = Event.objects.count()
    
    return render(request, 'core/insights.html', {
        'events': events,
        'chart_labels': json.dumps(chart_labels),
        'chart_values': json.dumps(chart_values),
        'avg_time': round(avg_time, 1),
        'total_events': total_events
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
    
    success_rate = (success_count / total_events * 100) if total_events > 0 else 0
    failure_rate = (failure_count / total_events * 100) if total_events > 0 else 0
    
    # Chart Data: Group by Day for the last 7 days
    daily_events = Event.objects.annotate(day=TruncDay('timestamp'))\
                               .values('day')\
                               .annotate(count=models.Count('id'))\
                               .order_by('day')
    
    chart_labels = [d['day'].strftime('%b %d') for d in daily_events]
    chart_values = [d['count'] for d in daily_events]

    return render(request, 'core/insights.html', {
        'events': events[:50],
        'total_events': total_events,
        'success_rate': round(success_rate, 1),
        'failure_rate': round(failure_rate, 1),
        'avg_time': round(avg_time, 2),
        'chart_labels': json.dumps(chart_labels),
        'chart_values': json.dumps(chart_values),
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

@login_required
def seed_database_view(request):
    """Secret view to trigger seed_data command from the browser."""
    if not request.user.is_staff:
        messages.error(request, "Unauthorized protocol access.")
        return redirect('index')
    
    from django.core.management import call_command
    try:
        call_command('seed_data')
        messages.success(request, "MESH SYNCHRONIZATION COMPLETE. NEW NODES INITIALIZED.")
    except Exception as e:
        messages.error(request, f"SYNCHRONIZATION FAILED: {str(e)}")
        
    return redirect('insights')

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def toggle_save(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    saved_post = SavedPost.objects.filter(user=request.user, post=post)
    if saved_post.exists():
        saved_post.delete()
    else:
        SavedPost.objects.create(user=request.user, post=post)
    return redirect(request.META.get('HTTP_REFERER', 'index'))
