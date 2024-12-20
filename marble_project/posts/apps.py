from django.apps import AppConfig

class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'  # Make sure this is 'posts' and NOT 'marble.posts'