from django.urls import path
from .views import SendMessageView, ConversationListView, MarkMessagesAsReadView, ConversationList

urlpatterns = [
    path("send/", SendMessageView.as_view(), name="send-message"),
    path("conversation/<int:user_id>/", ConversationListView.as_view(), name="conversation"),
    path("conversation/<int:user_id>/read/", MarkMessagesAsReadView.as_view(), name="mark-as-read"),
    path("conversations/", ConversationList.as_view(), name="conversations"),
]
