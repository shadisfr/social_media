from django.db import models
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("follow", "Follow"),
        ("like", "Like"),
        ("comment", "Comment"),
        ("message", "Message"),  
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")  
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_notifications") 
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)  
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.sender} {self.notification_type} {self.post if self.post else ''} for {self.user}"
