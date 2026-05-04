from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    open_to_work = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skill, related_name='users', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Post(models.Model):
    POST_TYPES = (
        ('general', 'General'),
        ('hiring', 'Hiring'),
        ('open_to_work', 'Open to Work'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='general')
    related_skills = models.ManyToManyField(Skill, related_name='posts', blank=True)

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp}"

class Event(models.Model):
    STATUS_CHOICES = (
        ('success', 'Success'),
        ('failure', 'Failure'),
    )
    event_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    processing_time = models.FloatField()  # in milliseconds
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='success')

    def __str__(self):
        return f"{self.event_type} - {self.status} ({self.timestamp})"
