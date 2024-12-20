from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from posts.views import (
    home,
    create_account,
    profile,
    account_logout,
    custom_login,
    follow_user,
    search_view,
    user_profile,
    change_profile_picture,
    update_description,
    create_post,
    like_post,
    post_detail,  # Ensure you import post_detail view
    view_post,    # Ensure you import view_post view
)

urlpatterns = [
    path('', home, name='home'),
    path('create-account/', create_account, name='create_account'),
    path('create-post/', create_post, name='create_post'),
    path('post/<int:post_id>/detail/', post_detail, name='post_detail'),  # Unique path for post_detail
    path('post/<int:post_id>/view/', view_post, name='view_post'),  # Unique path for view_post
    path('login/', custom_login, name='custom_login'),
    path('logout/', account_logout, name='account_logout'),
    path('profile/<int:user_id>/', profile, name='profile'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('user/<int:user_id>/', user_profile, name='user_profile'),
    path('search/', search_view, name='search'),  # Search view for user/posts
    path('profile/change-picture/', change_profile_picture, name='change_profile_picture'),
    path('update_description/', update_description, name='update_description'),
    path('like_post/<int:post_id>/', like_post, name='like_post'),
]

# Add media file handling during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
