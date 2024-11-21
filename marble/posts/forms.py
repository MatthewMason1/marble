from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'What\'s happening?',
                'rows': 3,
                'maxlength': 280  # Set a max length for the textarea
            }),
            'image': forms.ClearableFileInput(attrs={
                'accept': 'image/*',  # Allow only image files
            }),
            'video': forms.ClearableFileInput(attrs={
                'accept': 'video/*',  # Allow only video files
            }),
        }

    def clean_content(self):
        """Custom validation for content length."""
        content = self.cleaned_data.get('content')
        if len(content) > 280:
            raise forms.ValidationError("Content cannot exceed 280 characters.")
        return content

    def clean_image(self):
        """Validate uploaded image."""
        image = self.cleaned_data.get('image')
        if image and image.size > 5 * 1024 * 1024:  # Limit to 5 MB
            raise forms.ValidationError("Image file size must not exceed 5 MB.")
        return image

    def clean_video(self):
        """Validate uploaded video."""
        video = self.cleaned_data.get('video')
        if video and video.size > 10 * 1024 * 1024:  # Limit to 10 MB
            raise forms.ValidationError("Video file size must not exceed 10 MB.")
        return video

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Include the fields you want to use in the form
    
    def clean_content(self):
        """Custom validation for content length."""
        content = self.cleaned_data.get('content')
        if len(content) > 280:
            raise forms.ValidationError("Content cannot exceed 280 characters.")
        return content