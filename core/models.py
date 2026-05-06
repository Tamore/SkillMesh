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
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"

class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_posts_set')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} saved {self.post}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp}"

from django.utils import timezone

class Event(models.Model):
    STATUS_CHOICES = (
        ('success', 'Success'),
        ('failure', 'Failure'),
    )
    event_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)
    processing_time = models.FloatField()  # in milliseconds
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='success')

    def __str__(self):
        return f"{self.event_type} - {self.status} ({self.timestamp})"

# --- SIGNALS ---
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def log_user_creation(sender, instance, created, **kwargs):
    """Automatically log an event when a new identity node is initialized."""
    if created:
        Event.objects.create(
            event_type='IdentityCreated',
            status='success',
            processing_time=150.0  # Estimated protocol latency
        )

@receiver(post_save, sender=Post)
def log_post_creation(sender, instance, created, **kwargs):
    """Automatically log an event when a new signal is broadcast."""
    if created:
        Event.objects.create(
            event_type='PostCreated',
            status='success',
            processing_time=85.0
        )

@receiver(post_save, sender=UserProfile)
def log_profile_update(sender, instance, created, **kwargs):
    """Automatically log an event when a profile node is modified."""
    if not created:
        Event.objects.create(
            event_type='ProfileUpdated',
            status='success',
            processing_time=45.0
        )
