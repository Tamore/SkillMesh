# core/services.py
# This file will contain all the business logic for the SkillMesh application.
# It is a key part of our architecture to keep logic out of views.

import time
from datetime import datetime
from django.contrib.auth.models import User
from .models import Event, UserProfile, Skill, Post, Message

from django.db import transaction, IntegrityError

def log_event(event_type, start_time, status="success"):
    """
    Calculates processing time and stores the event in the database.
    """
    end_time = time.time()
    processing_time = (end_time - start_time) * 1000  # in milliseconds
    
    event = Event.objects.create(
        event_type=event_type,
        processing_time=processing_time,
        status=status
    )
    return event

@transaction.atomic
def register_user(username, email, password, bio=""):
    """
    Registers a new user, creates a profile, and logs the UserRegistered event.
    """
    start_time = time.time()
    
    # 1. Create User
    user = User.objects.create_user(username=username, email=email, password=password)
    
    # 2. Update Profile (Signals usually create the profile automatically)
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.bio = bio
    profile.save()
    
    # 3. Log Event
    log_event("UserRegistered", start_time)
    
    return user

def update_profile(user, bio=None, profile_picture=None, open_to_work=None):
    """
    Updates the user profile and logs the ProfileUpdated event.
    """
    start_time = time.time()
    profile = user.profile
    
    if bio is not None:
        profile.bio = bio
    if profile_picture is not None:
        profile.profile_picture = profile_picture
    if open_to_work is not None:
        profile.open_to_work = open_to_work
        
    profile.save()
    
    log_event("ProfileUpdated", start_time)
    return profile

def add_skill_to_user(user, skill_name):
    """
    Adds a skill to the user profile and logs the SkillAdded event.
    """
    start_time = time.time()
    
    # Get or create the skill
    skill, created = Skill.objects.get_or_create(name=skill_name.strip().lower())
    
    # Add to user's skills
    user.profile.skills.add(skill)
    
    log_event("SkillAdded", start_time)
    return skill

def create_post(user, content, post_type="general", skill_ids=None):
    """
    Creates a new post, tags skills, and logs the PostCreated event.
    """
    start_time = time.time()
    
    post = Post.objects.create(
        user=user,
        content=content,
        post_type=post_type
    )
    
    if skill_ids:
        post.related_skills.set(skill_ids)
        
    log_event("PostCreated", start_time)
    return post

def send_message(sender, receiver_username, content):
    """
    Sends a message to another user and logs the MessageSent event.
    """
    start_time = time.time()
    
    receiver = User.objects.get(username=receiver_username)
    
    message = Message.objects.create(
        sender=sender,
        receiver=receiver,
        content=content
    )
    
    log_event("MessageSent", start_time)
    return message

from django.db.models import Q

def search_users_by_skill(query):
    """
    Finds users by skill, username, or bio.
    """
    if not query:
        return UserProfile.objects.none()
        
    query_str = query.strip().lower()
    return UserProfile.objects.filter(
        Q(skills__name__icontains=query_str) |
        Q(user__username__icontains=query_str) |
        Q(bio__icontains=query_str)
    ).distinct()
