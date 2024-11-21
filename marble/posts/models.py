from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import FileExtensionValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        default='default_profile.png',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])]
    )
    banner = models.ImageField(
        upload_to='banners/',
        default='default_banner.png',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])]
    )
    description = models.CharField(max_length=20, blank=True, null=True)  # Limited to 20 characters
    last_active = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='Untitled')  # Set a default value here
    content = models.TextField()
    image = models.ImageField(
        upload_to='images/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])]
    )
    video = models.FileField(
        upload_to='videos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov'])]
    )
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)  # Moved outside of the image field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Post: {self.content[:20]}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked '{self.post.content[:20]}'"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation

    def __str__(self):
        return self.content


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

    @classmethod
    def is_following(cls, follower, followed):
        return cls.objects.filter(follower=follower, followed=followed).exists()


class AccountCreationAttempt(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def is_blocked(self):
        """Checks if the account creation is blocked based on the attempts."""
        recent_attempts = AccountCreationAttempt.objects.filter(
            ip_address=self.ip_address,
            timestamp__gte=timezone.now() - timezone.timedelta(hours=12)
        )
        return recent_attempts.count() >= 4  # Adjust the limit as needed

    def __str__(self):
        return f"Attempt from {self.ip_address} at {self.timestamp}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile instance when a User is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile instance when the User is saved."""
    instance.userprofile.save()
