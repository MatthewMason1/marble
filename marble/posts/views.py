from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Follow, AccountCreationAttempt
from django.contrib.auth.models import User
from django import forms
from django.http import HttpResponseRedirect
from django.http import JsonResponse 
from django.utils import timezone
from datetime import timedelta
from .forms import PostForm
from .models import Post, Comment
from .forms import CommentForm



# Default profile picture URL
DEFAULT_PROFILE_PICTURE_URL = "https://tr.rbxcdn.com/180DAY-4ab626f2df7ffe788a3b06500d127a99/420/420/Hat/Webp/noFilter"

# Helper function to get the profile picture URL
def get_profile_picture_url(user_profile):
    """Returns the profile picture URL or the default URL if none is set."""
    return user_profile.profile_picture.url if user_profile.profile_picture else DEFAULT_PROFILE_PICTURE_URL

def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/apost.html', {'post': post})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Only proceed if it's a POST request
    if request.method == 'POST':
        # Toggle like/unlike action
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        # Redirect to the same page (using request.META['HTTP_REFERER'] will go back to the referring page)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # If no referer, go to home

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # If not POST, go back to previous page
    
@login_required
def post_detail(request, post_id):
    # Get the post object
    post = get_object_or_404(Post, id=post_id)
    
    # Fetch all comments related to this post
    comments = Comment.objects.filter(post=post)
    
    # Handle the form submission
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # Create the comment instance but don't save yet
            comment = comment_form.save(commit=False)
            # Associate the logged-in user with the comment
            comment.user = request.user
            # Associate the current post with the comment
            comment.post = post
            # Save the comment
            comment.save()
            # Redirect to the same post page to display the new comment
            return redirect('post_detail', post_id=post.id)
    else:
        # Initialize an empty form if it's a GET request
        comment_form = CommentForm()

    # Render the template with the post, comments, and form
    return render(request, 'posts/apost.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form  # Pass the form to the template
    })

@login_required
def change_profile_picture(request):
    """Handle changing the user's profile picture."""
    if request.method == 'POST' and 'profile_picture' in request.FILES:
        user_profile = request.user.userprofile
        user_profile.profile_picture = request.FILES['profile_picture']
        user_profile.save()
        messages.success(request, 'Profile picture updated successfully.')
    else:
        messages.error(request, 'Profile update failed. Please try again.')
    return redirect('profile', user_id=request.user.id)

@login_required
def profile(request, user_id=None):
    """Render the user's profile page and handle profile picture updates."""
    user = get_object_or_404(User, id=user_id) if user_id else request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    # Allow users to update their own profile picture
    if request.method == 'POST' and user == request.user:
        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
            
            # Optional: Add validation for the image type or size
            try:
                # Validate image (Example: check file size)
                if profile_picture.size > 5 * 1024 * 1024:  # Limit to 5MB
                    raise ValidationError("File size exceeds 5MB.")
                
                # Save the profile picture to the user's profile
                user_profile.profile_picture = profile_picture
                user_profile.save()
                messages.success(request, 'Profile picture updated successfully.')
            except ValidationError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'No profile picture uploaded.')
        
        return redirect('profile', user_id=request.user.id)

    # Render profile with the appropriate profile picture URL
    profile_picture_url = user_profile.profile_picture.url if user_profile.profile_picture else None

    return render(request, 'posts/profile.html', {
        'user_profile': user_profile,
        'profile_picture_url': profile_picture_url
    })

def home(request):
    """Render the home page with the most recent users."""
    recent_users = UserProfile.objects.order_by('-user__date_joined')[:8]
    return render(request, 'posts/index.html', {
        'recent_users': recent_users,
        'DEFAULT_PROFILE_PICTURE_URL': DEFAULT_PROFILE_PICTURE_URL,
    })

def get_client_ip(request):
    """Helper function to get the client's IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post

@login_required
def create_post(request):
    if request.method == 'POST':
        # Retrieve data from the request
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')  # Get the image from the form
        video = request.FILES.get('video')  # Get the video from the form

        # Create a new Post object
        post = Post(
            user=request.user,  # Assign the current logged-in user
            title=title,
            content=content,
            image=image,
            video=video
        )
        post.save()  # Save the post object to the database

        return redirect('home')  # Redirect to the homepage or wherever appropriate

    return render(request, 'posts/create_post.html')  # Render the form if GET request


def create_account(request):
    """Handle the account creation process."""
    ip_address = get_client_ip(request)
    
    # Check for existing attempt records in the last 12 hours
    recent_attempts = AccountCreationAttempt.objects.filter(
        ip_address=ip_address,
        timestamp__gte=timezone.now() - timedelta(hours=12)
    )

    if recent_attempts.exists() and recent_attempts.first().is_blocked():
        messages.error(request, "You have been timed out.")
        return redirect('home')  # Redirect to homepage or an error page

    # Proceed with account creation
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Create account
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. Welcome!')

            # Log the successful attempt
            AccountCreationAttempt.objects.create(ip_address=ip_address)
            return redirect('profile', user_id=user.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'posts/create_account.html', {'form': form})

def custom_login(request):
    """Handle user login logic."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            # Ensure the user has a profile
            if not hasattr(user, 'userprofile'):
                UserProfile.objects.create(user=user)

            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('profile', user_id=user.id)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'posts/login.html')

@login_required
def account_logout(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
def follow_user(request, user_id):
    """Handle the action of following or unfollowing another user."""
    user_to_follow = get_object_or_404(User, id=user_id)

    if request.user != user_to_follow:
        follow, created = Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
        if created:
            messages.success(request, f'You are now following {user_to_follow.username}.')
        else:
            follow.delete()  # Remove the follow relationship
            messages.success(request, f'You have unfollowed {user_to_follow.username}.')
    else:
        messages.warning(request, "You can't follow yourself.")

    return redirect('user_profile', user_id=user_id)

def user_profile(request, user_id):
    """Render another user's public profile page."""
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)
    
    # Get the followers of the user
    followers = Follow.objects.filter(followed=user)
    is_following = Follow.objects.filter(follower=request.user, followed=user).exists() if request.user.is_authenticated else False
    
    # Fetch the user's posts
    posts = Post.objects.filter(user=user).order_by('-created_at')  # Adjust ordering as needed

    return render(request, 'posts/user.html', {
        'user_profile': user_profile,
        'followers': followers,
        'is_following': is_following,
        'profile_picture_url': get_profile_picture_url(user_profile),
        'posts': posts,  # Pass the posts to the template
    })

@login_required
def update_description(request):
    """Handle updating the user's account description."""
    if request.method == 'POST':
        description = request.POST.get('description')
        request.user.userprofile.description = description
        request.user.userprofile.save()
        messages.success(request, 'Description updated successfully.')
    return redirect('profile', user_id=request.user.id)

class CustomUserCreationForm(UserCreationForm):
    """Custom form for user creation with custom validation."""
    
    error_messages = {
        'password_mismatch': "The passwords you entered do not match. Please try again.",
        'duplicate_username': "The username you entered is already taken. Please choose a different one.",
    }
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_username(self):
        """Custom validation for the username field."""
        username = self.cleaned_data.get('username')
        if len(username) < 5:
            raise forms.ValidationError("Username must be at least 5 characters long.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(self.error_messages['duplicate_username'])
        return username
from django.db.models import Q  # Import Q for complex queries

def search_view(request):
    """Handle search queries for user accounts."""
    query = request.GET.get('query', '')
    results = []

    if query:
        # Search for usernames that match the query (case-insensitive)
        results = User.objects.filter(Q(username__icontains=query))

    return render(request, 'posts/results.html', {
        'results': results,
        'query': query,
    })


def home(request):
    recent_users = UserProfile.objects.order_by('-user__date_joined')[:8]
    posts = Post.objects.all().order_by('-created_at')  # Fetch posts to display
    return render(request, 'posts/index.html', {
        'recent_users': recent_users,
        'posts': posts,
        'DEFAULT_PROFILE_PICTURE_URL': DEFAULT_PROFILE_PICTURE_URL,
    })

