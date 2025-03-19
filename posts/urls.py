from django.urls import path
from .views import PostListCreateView, PostDetailView, LikePostView, CommentListCreateView, TimelineFeedView

urlpatterns = [
    path("", PostListCreateView.as_view(), name="post-list"),
    path("<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("<int:post_id>/like/", LikePostView.as_view(), name="like-post"),
    path("<int:post_id>/comments/", CommentListCreateView.as_view(), name="comment-list"),
    path("feed/", TimelineFeedView.as_view(), name="timeline-feed"),
]
